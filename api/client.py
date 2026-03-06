import httpx
import socket
import asyncio
from typing import Dict, Any, Optional, List
from structlog import get_logger

from config.settings import settings
from config.constants import META_GRAPH_BASE_URL
from api.rate_limiter import rate_limiter_instance
from api.error_handler import MetaAPIError, get_error_message

logger = get_logger(__name__)

async def resolve_meta_host(host: str = "graph.facebook.com") -> Optional[str]:
    """Tries to resolve the Meta host using system DNS, then fallbacks to DoH."""
    # 1. Try system DNS
    try:
        return await asyncio.to_thread(socket.gethostbyname, host)
    except Exception:
        logger.warning("System DNS failed for Meta host, trying DoH", host=host)
    
    # 2. Try Google DNS-over-HTTPS
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://dns.google/resolve", params={"name": host, "type": "A"}, timeout=3.0)
            if res.status_code == 200:
                data = res.json()
                ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
                if ips:
                    return ips[0]
    except Exception as e:
        logger.warning("Google DoH failed", error=str(e))

    # 3. Try Cloudflare DNS-over-HTTPS
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://cloudflare-dns.com/query", params={"name": host, "type": "A"}, 
                                   headers={"accept": "application/dns-json"}, timeout=3.0)
            if res.status_code == 200:
                data = res.json()
                ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
                if ips:
                    return ips[0]
    except Exception as e:
        logger.warning("Cloudflare DoH failed", error=str(e))
        
    return None

class MetaAPIClient:
    _instance = None
    
    def __init__(self, resolved_ip: Optional[str] = None):
        self.host = "graph.facebook.com"
        self.base_url = META_GRAPH_BASE_URL
        
        if resolved_ip:
            logger.info("Using manual IP for Meta API", host=self.host, ip=resolved_ip)
            # We must use the IP in the URL but keep the Host header and SNI
            # A bit tricky with standard httpx without complex transports
            # For now, we'll swap the base_url but it might hit SSL issues
            # Actually, we can use a transport that overrides the destination
            self.base_url = self.base_url.replace(self.host, resolved_ip)
            
        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_connections=20),
            # If we use IP, we might need to disable verification or handle SNI
            verify=True if not resolved_ip else False 
        )
        self.access_token = settings.META_ACCESS_TOKEN
        self.resolved_ip = resolved_ip

    @classmethod
    async def initialize(cls):
        if cls._instance is None:
            # Try to resolve host first
            ip = await resolve_meta_host()
            # Only use IP fallback if hostname resolution failed locally
            try:
                socket.gethostbyname("graph.facebook.com")
                cls._instance = cls()
            except Exception:
                cls._instance = cls(resolved_ip=ip)
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

    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Adds Host header if using manual IP."""
        full_headers = (headers or {}).copy()
        if self.resolved_ip:
            full_headers["Host"] = self.host
        return full_headers

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
            headers = self._prepare_headers(kwargs.get("headers"))
            kwargs["headers"] = headers
            
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
