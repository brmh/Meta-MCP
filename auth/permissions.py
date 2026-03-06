from typing import List
from structlog import get_logger

logger = get_logger(__name__)

# Basic permissions we want to ensure
# Ads Management is the biggest one
REQUIRED_PERMISSIONS = [
    "ads_read",
    "ads_management",
    "business_management",
    "pages_read_engagement",
    "pages_manage_ads",
    "instagram_basic",
    "instagram_content_publish",
    "catalog_management",
    "leads_retrieval",
    "read_insights",
]

class PermissionAuditor:
    @staticmethod
    def identify_missing_permissions(granted_permissions: List[str]) -> List[str]:
        """Identifies any missing permissions from the standard required list."""
        missing = [p for p in REQUIRED_PERMISSIONS if p not in granted_permissions]
        return missing

    @staticmethod
    def audit_permissions(granted_scopes: List[str]):
        """Logs and returns missing permissions. Non-blocking."""
        missing = PermissionAuditor.identify_missing_permissions(granted_scopes)
        if missing:
            logger.warning("Missing recommended permissions", missing=missing)
        else:
            logger.info("All recommended permissions are granted.")
        return missing
