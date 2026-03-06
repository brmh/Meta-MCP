import httpx
from config.settings import settings
from config.constants import META_GRAPH_BASE_URL
from auth.permissions import PermissionAuditor
from api.error_handler import MetaAPIError, get_error_message
from structlog import get_logger

logger = get_logger(__name__)

class TokenManager:
    @staticmethod
    async def exchange_for_long_lived_token(short_lived_token: str) -> str:
        """Exchanges a short-lived user access token for a long-lived one."""
        if not settings.META_APP_ID or not settings.META_APP_SECRET:
            raise ValueError("App ID and App Secret must be set for token exchange.")
            
        async with httpx.AsyncClient(base_url=META_GRAPH_BASE_URL) as client:
            response = await client.get("/oauth/access_token", params={
                "grant_type": "fb_exchange_token",
                "client_id": settings.META_APP_ID,
                "client_secret": settings.META_APP_SECRET,
                "fb_exchange_token": short_lived_token
            })
            
            data = response.json()
            if "error" in data:
                raise MetaAPIError(f"OAuth Error: {data['error'].get('message')}")
                
            return data.get("access_token")

    @staticmethod
    async def validate_token(token: str) -> dict:
        """Validates token and returns scopes, expiry, and user id."""
        async with httpx.AsyncClient(base_url=META_GRAPH_BASE_URL) as client:
            response = await client.get("/debug_token", params={
                "input_token": token,
                "access_token": f"{settings.META_APP_ID}|{settings.META_APP_SECRET}" if settings.META_APP_ID and settings.META_APP_SECRET else token # Fallback to using token itself if app secret isn't available
            })
            data = response.json()
            if "error" in data:
                 raise MetaAPIError(f"Token Debug Error: {data['error'].get('message')}")
            
            # The structure is usually {"data": {"is_valid": true, "scopes": [...]}}
            return data.get("data", {})
            
    @staticmethod
    async def check_permissions(token: str) -> dict:
        """Returns missing vs granted scopes"""
        info = await TokenManager.validate_token(token)
        granted_scopes = info.get("scopes", [])
        missing = PermissionAuditor.identify_missing_permissions(granted_scopes)
        
        return {
            "granted": granted_scopes,
            "missing": missing,
            "is_valid": info.get("is_valid", False)
        }

    @staticmethod
    async def validate_on_startup() -> None:
        """Validates token on server start, fail fast if completely invalid."""
        if not settings.META_ACCESS_TOKEN:
             logger.warning("No META_ACCESS_TOKEN provided. Some tools may fail.")
             return
        
        try:
             info = await TokenManager.validate_token(settings.META_ACCESS_TOKEN)
             if not info.get("is_valid"):
                  logger.error("Startup Validation Failed: The provided token is invalid or expired.")
             else:
                  logger.info("Startup Validation Success: Token is valid.")
                  PermissionAuditor.audit_permissions(info.get("scopes", []))
        except Exception as e:
             logger.warning(f"Could not fully validate token on startup: {e}")
