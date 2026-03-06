import httpx
from typing import Dict, Any, Optional, List
from structlog import get_logger

from config.settings import settings
from config.constants import META_GRAPH_BASE_URL
from api.rate_limiter import rate_limiter_instance
from api.error_handler import MetaAPIError, get_error_message

logger = get_logger(__name__)

class MetaAPIClient:
    _instance = None
    
    def __init__(self):
        self.session = httpx.AsyncClient(
            base_url=META_GRAPH_BASE_URL,
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_connections=20)
        )
        self.access_token = settings.META_ACCESS_TOKEN

    @classmethod
    async def initialize(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.session.aclose()
            cls._instance = None

    def _prepare_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Injects access token into params."""
        full_params = params.copy()
        if "access_token" not in full_params:
            full_params["access_token"] = self.access_token
        return full_params

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Parses the response, checks rate limits, and throws MetaAPIError on failure."""
        
        # Check rate limit headers globally (not heavily enforced in this simple version, but hooked up)
        # rate_limiter_instance.handle_rate_limit_headers(response.headers)
        
        try:
            data = response.json()
        except Exception:
            raise MetaAPIError(f"Failed to parse JSON response: {response.text}", 
                               error_code=response.status_code)

        if "error" in data:
            error_data = data["error"]
            code = error_data.get("code")
            subcode = error_data.get("error_subcode")
            fbtrace_id = error_data.get("fbtrace_id")
            message = error_data.get("message", get_error_message(code))
            
            logger.error("Meta API Error", code=code, subcode=subcode, fbtrace_id=fbtrace_id, message=message)
            raise MetaAPIError(message, error_code=code, error_subcode=subcode, fbtrace_id=fbtrace_id)

        return data

    async def _execute_with_retries(self, method: str, endpoint: str, **kwargs):
        """Wrapper to pass the request to the rate limiter."""
        
        async def _call():
            if method == "GET":
                 return await self.session.get(endpoint, **kwargs)
            elif method == "POST":
                 return await self.session.post(endpoint, **kwargs)
            elif method == "DELETE":
                 return await self.session.delete(endpoint, **kwargs)
            else:
                 raise ValueError(f"Unsupported method: {method}")

        # The rate limiter handles the await _call() and exceptions
        response = await rate_limiter_instance.execute_with_retries(_call)
        return self._handle_response(response)

    async def get(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Performs a GET request."""
        full_params = self._prepare_params(params)
        
        # Convert list params to comma separated strings if needed by meta api
        for k, v in full_params.items():
            if isinstance(v, list):
                full_params[k] = ",".join(map(str,v))
                
        return await self._execute_with_retries("GET", endpoint, params=full_params)

    async def post(self, endpoint: str, data: Dict[str, Any] = {}, files: Dict[str, Any] = None) -> Dict[str, Any]:
        """Performs a POST request."""
        # Meta API typically expects data as application/x-www-form-urlencoded or multipart/form-data
        # We append access token to the payload
        full_data = self._prepare_params(data)
        
        # Clean up data by dumping dicts to json strings if needed by the Graph API for nested objects 
        # (Usually handled before calling post, but good practice to be aware of)
        import json
        for k, v in full_data.items():
             if isinstance(v, (dict, list)) and k != "access_token":
                  full_data[k] = json.dumps(v)
        
        if files:
            # When sending files, data goes into data=, files goes into files=
            return await self._execute_with_retries("POST", endpoint, data=full_data, files=files)
        else:
            return await self._execute_with_retries("POST", endpoint, data=full_data)

    async def delete(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Performs a DELETE request."""
        full_params = self._prepare_params(params)
        return await self._execute_with_retries("DELETE", endpoint, params=full_params)

    async def paginate(self, endpoint: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Auto-follows pagination cursors and returns all results."""
        all_data = []
        current_endpoint = endpoint
        current_params = params.copy()

        while True:
            response = await self.get(current_endpoint, current_params)
            
            data = response.get("data", [])
            all_data.extend(data)
            
            paging = response.get("paging", {})
            cursors = paging.get("cursors", {})
            after = cursors.get("after")
            next_url = paging.get("next")
            
            if not after or not next_url:
                break
                
            # For the next request, we just need the 'after' cursor and same params
            current_params["after"] = after

        return all_data
