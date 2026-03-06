from enum import Enum

# Meta API Configuration
META_API_VERSION = "v21.0"
META_GRAPH_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"

# Retry Configuration
MAX_RETRIES = 3
BASE_BACKOFF = 2.0
MAX_BACKOFF = 64.0

class Objective(str, Enum):
    OUTCOME_AWARENESS = "OUTCOME_AWARENESS"
    OUTCOME_TRAFFIC = "OUTCOME_TRAFFIC"
    OUTCOME_ENGAGEMENT = "OUTCOME_ENGAGEMENT"
    OUTCOME_LEADS = "OUTCOME_LEADS"
    OUTCOME_APP_PROMOTION = "OUTCOME_APP_PROMOTION"
    OUTCOME_SALES = "OUTCOME_SALES"

class Status(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"

VALID_METRICS = [
    "impressions", "reach", "frequency", "spend", "clicks",
    "unique_clicks", "ctr", "unique_ctr", "cpc", "cpm", "cpp",
    "actions", "action_values", "cost_per_action_type",
    "conversions", "cost_per_conversion", "purchase_roas",
    "video_views", "video_p25_watched_actions", "video_p50_watched_actions",
    "video_p75_watched_actions", "video_p100_watched_actions",
    "video_avg_time_watched_actions", "video_thruplay_watched_actions",
    "outbound_clicks", "outbound_clicks_ctr", "unique_outbound_clicks",
    "social_spend", "canvas_avg_view_time", "canvas_avg_view_percent",
    "instant_experience_clicks_to_open", "instant_experience_clicks_to_start",
    "inline_link_clicks", "inline_post_engagement", "website_ctr",
    "objective", "quality_ranking", "engagement_rate_ranking",
    "conversion_rate_ranking", "account_name", "campaign_name",
    "adset_name", "ad_name", "date_start", "date_stop"
]

VALID_BREAKDOWNS = [
    "age", "gender", "country", "region", "dma",
    "impression_device", "platform_position", "publisher_platform",
    "device_platform", "product_id",
    "hourly_stats_aggregated_by_advertiser_time_zone",
    "hourly_stats_aggregated_by_audience_time_zone"
]

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
