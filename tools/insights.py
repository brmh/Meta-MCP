import asyncio
from typing import Optional, Literal, List, Annotated, Dict, Any, Union
from pydantic import Field
from api.client import MetaAPIClient

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

def _prepare_insights_params(
    date_preset: Optional[str], time_range: Optional[Dict[str, str]], time_increment: Union[int, str],
    level: str, fields: List[str], breakdowns: List[str], action_breakdowns: List[str],
    filtering: List[Dict[str, Any]], sort: List[str], limit: Optional[int] = None, after: Optional[str] = None
) -> dict:
    params = {"level": level}
    if date_preset: params["date_preset"] = date_preset
    if time_range: params["time_range"] = time_range
    if time_increment: params["time_increment"] = time_increment
    if fields: params["fields"] = fields
    if breakdowns: params["breakdowns"] = breakdowns
    if action_breakdowns: params["action_breakdowns"] = action_breakdowns
    if filtering: params["filtering"] = filtering
    if sort: params["sort"] = sort
    if limit: params["limit"] = limit
    if after: params["after"] = after
    return params

async def get_account_insights(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    date_preset: Annotated[Optional[str], Field(description="Date preset (e.g. last_30d).")] = "last_30d",
    time_range: Annotated[Optional[Dict[str, str]], Field(description="Exact time range {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}.")] = None,
    time_increment: Annotated[Union[int, str], Field(description="1 for daily, 'all_days' or interval.")] = 1,
    level: Annotated[Literal["account", "campaign", "adset", "ad"], Field(description="Aggregation level.")] = "account",
    fields: Annotated[List[str], Field(description="List of metrics to fetch from VALID_METRICS.")] = [],
    breakdowns: Annotated[List[str], Field(description="List of breakdowns from VALID_BREAKDOWNS.")] = [],
    action_breakdowns: Annotated[List[str], Field(description="E.g., ['action_type'].")] = ["action_type"],
    filtering: Annotated[List[Dict[str, Any]], Field(description="List of filters [{field, operator, value}].")] = [],
    sort: Annotated[List[str], Field(description="E.g. ['spend_descending'].")] = ["spend_descending"],
    limit: Annotated[int, Field(description="Results per page.")] = 25,
    after: Annotated[Optional[str], Field(description="Cursor string.")] = None
) -> dict:
    """Synchronous insights fetch for an ad account."""
    client = await MetaAPIClient.initialize()
    params = _prepare_insights_params(date_preset, time_range, time_increment, level, fields, breakdowns, action_breakdowns, filtering, sort, limit, after)
    return await client.get(f"/{ad_account_id}/insights", params=params)

async def get_campaign_insights(
    campaign_id: Annotated[str, Field(description="Campaign ID.")],
    date_preset: Annotated[Optional[str], Field(description="Date preset (e.g. last_30d).")] = "last_30d",
    time_range: Annotated[Optional[Dict[str, str]], Field(description="Exact time range {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}.")] = None,
    time_increment: Annotated[Union[int, str], Field(description="1 for daily, 'all_days' or interval.")] = 1,
    level: Annotated[Literal["account", "campaign", "adset", "ad"], Field(description="Aggregation level.")] = "campaign",
    fields: Annotated[List[str], Field(description="List of metrics to fetch from VALID_METRICS.")] = [],
    breakdowns: Annotated[List[str], Field(description="List of breakdowns from VALID_BREAKDOWNS.")] = [],
    action_breakdowns: Annotated[List[str], Field(description="E.g., ['action_type'].")] = ["action_type"],
    filtering: Annotated[List[Dict[str, Any]], Field(description="List of filters [{field, operator, value}].")] = [],
    sort: Annotated[List[str], Field(description="E.g. ['spend_descending'].")] = ["spend_descending"],
    limit: Annotated[int, Field(description="Results per page.")] = 25,
    after: Annotated[Optional[str], Field(description="Cursor string.")] = None
) -> dict:
    """Synchronous insights fetch for a campaign."""
    client = await MetaAPIClient.initialize()
    params = _prepare_insights_params(date_preset, time_range, time_increment, level, fields, breakdowns, action_breakdowns, filtering, sort, limit, after)
    return await client.get(f"/{campaign_id}/insights", params=params)

async def get_adset_insights(
    adset_id: Annotated[str, Field(description="Ad Set ID.")],
    date_preset: Annotated[Optional[str], Field(description="Date preset (e.g. last_30d).")] = "last_30d",
    time_range: Annotated[Optional[Dict[str, str]], Field(description="Exact time range {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}.")] = None,
    time_increment: Annotated[Union[int, str], Field(description="1 for daily, 'all_days' or interval.")] = 1,
    level: Annotated[Literal["account", "campaign", "adset", "ad"], Field(description="Aggregation level.")] = "adset",
    fields: Annotated[List[str], Field(description="List of metrics to fetch from VALID_METRICS.")] = [],
    breakdowns: Annotated[List[str], Field(description="List of breakdowns from VALID_BREAKDOWNS.")] = [],
    action_breakdowns: Annotated[List[str], Field(description="E.g., ['action_type'].")] = ["action_type"],
    filtering: Annotated[List[Dict[str, Any]], Field(description="List of filters [{field, operator, value}].")] = [],
    sort: Annotated[List[str], Field(description="E.g. ['spend_descending'].")] = ["spend_descending"],
    limit: Annotated[int, Field(description="Results per page.")] = 25,
    after: Annotated[Optional[str], Field(description="Cursor string.")] = None
) -> dict:
    """Synchronous insights fetch for an ad set."""
    client = await MetaAPIClient.initialize()
    params = _prepare_insights_params(date_preset, time_range, time_increment, level, fields, breakdowns, action_breakdowns, filtering, sort, limit, after)
    return await client.get(f"/{adset_id}/insights", params=params)

async def get_ad_insights(
    ad_id: Annotated[str, Field(description="Ad ID.")],
    date_preset: Annotated[Optional[str], Field(description="Date preset (e.g. last_30d).")] = "last_30d",
    time_range: Annotated[Optional[Dict[str, str]], Field(description="Exact time range {'since': 'YYYY-MM-DD', 'until': 'YYYY-MM-DD'}.")] = None,
    time_increment: Annotated[Union[int, str], Field(description="1 for daily, 'all_days' or interval.")] = 1,
    level: Annotated[Literal["account", "campaign", "adset", "ad"], Field(description="Aggregation level.")] = "ad",
    fields: Annotated[List[str], Field(description="List of metrics to fetch from VALID_METRICS.")] = [],
    breakdowns: Annotated[List[str], Field(description="List of breakdowns from VALID_BREAKDOWNS.")] = [],
    action_breakdowns: Annotated[List[str], Field(description="E.g., ['action_type'].")] = ["action_type"],
    filtering: Annotated[List[Dict[str, Any]], Field(description="List of filters [{field, operator, value}].")] = [],
    sort: Annotated[List[str], Field(description="E.g. ['spend_descending'].")] = ["spend_descending"],
    limit: Annotated[int, Field(description="Results per page.")] = 25,
    after: Annotated[Optional[str], Field(description="Cursor string.")] = None
) -> dict:
    """Synchronous insights fetch for an ad."""
    client = await MetaAPIClient.initialize()
    params = _prepare_insights_params(date_preset, time_range, time_increment, level, fields, breakdowns, action_breakdowns, filtering, sort, limit, after)
    return await client.get(f"/{ad_id}/insights", params=params)

async def create_async_report(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    level: Annotated[str, Field(description="Aggregation level.")],
    date_preset: Annotated[Optional[str], Field(description="Preset.")] = None, 
    time_range: Annotated[Optional[Dict[str, str]], Field(description="Range.")] = None,
    time_increment: Annotated[Union[int, str], Field(description="Increment.")] = "all_days",
    fields: Annotated[List[str], Field(description="Metrics.")] = [], 
    breakdowns: Annotated[List[str], Field(description="Breakdowns.")] = [],
    action_breakdowns: Annotated[List[str], Field(description="Action Breakdowns.")] = [], 
    filtering: Annotated[List[Dict[str, Any]], Field(description="Filters.")] = [], 
    sort: Annotated[List[str], Field(description="Sort order.")] = []
) -> dict:
    """Creates an asynchronous report job."""
    client = await MetaAPIClient.initialize()
    params = _prepare_insights_params(date_preset, time_range, time_increment, level, fields, breakdowns, action_breakdowns, filtering, sort)
    return await client.post(f"/{ad_account_id}/insights", data=params)

async def get_async_report_status(report_run_id: Annotated[str, Field(description="Report Run ID.")]) -> dict:
    """Checks status of an async report."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{report_run_id}")

async def get_async_report_results(
    report_run_id: Annotated[str, Field(description="Report Run ID.")], 
    limit: Annotated[int, Field(description="Results limit.")] = 100, 
    after: Annotated[Optional[str], Field(description="Cursor sequence.")] = None
) -> dict:
    """Fetches the generated results of an async report."""
    client = await MetaAPIClient.initialize()
    params = {"limit": limit}
    if after: params["after"] = after
    return await client.get(f"/{report_run_id}/insights", params=params)

async def wait_for_async_report(
    report_run_id: Annotated[str, Field(description="Report Run ID.")], 
    poll_interval: Annotated[int, Field(description="Seconds to wait between polls.")] = 5, 
    timeout: Annotated[int, Field(description="Max seconds to wait for completion.")] = 300
) -> dict:
    """Waits for an async report to complete and fetches first page of results."""
    client = await MetaAPIClient.initialize()
    elapsed = 0
    while elapsed < timeout:
        status_res = await client.get(f"/{report_run_id}")
        status = status_res.get("async_percent_completion", 0)
        async_status = status_res.get("async_status")
        
        if async_status == "Job Completed":
            return await get_async_report_results(report_run_id, limit=25)
        if async_status in ["Job Failed", "Job Skipped"]:
            raise Exception(f"Async report failed or skipped. Status: {async_status}")
            
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
        
    raise TimeoutError(f"Async report {report_run_id} did not complete within {timeout} seconds.")

async def get_demographic_breakdown(
    entity_type: Annotated[str, Field(description="account, campaign, adset, ad.")], 
    entity_id: Annotated[str, Field(description="The ID.")], 
    breakdown: Annotated[str, Field(description="E.g., age, gender.")], 
    date_preset: Annotated[str, Field(description="Date preset.")] = "last_30d"
) -> dict:
    """Gets demographic breakdown insights."""
    client = await MetaAPIClient.initialize()
    params = {"level": entity_type, "breakdowns": breakdown, "date_preset": date_preset}
    return await client.get(f"/{entity_id}/insights", params=params)

async def get_platform_breakdown(
    entity_type: Annotated[str, Field(description="E.g., account.")], 
    entity_id: Annotated[str, Field(description="The ID.")], 
    date_preset: Annotated[str, Field(description="Date.")] = "last_30d"
) -> dict:
    """Gets publisher platform reporting."""
    client = await MetaAPIClient.initialize()
    params = {"level": entity_type, "breakdowns": "publisher_platform,platform_position", "date_preset": date_preset}
    return await client.get(f"/{entity_id}/insights", params=params)

async def get_device_breakdown(
    entity_type: Annotated[str, Field(description="Type.")], 
    entity_id: Annotated[str, Field(description="The ID.")], 
    date_preset: Annotated[str, Field(description="Date.")] = "last_30d"
) -> dict:
    """Gets device impression breakdowns."""
    client = await MetaAPIClient.initialize()
    params = {"level": entity_type, "breakdowns": "impression_device", "date_preset": date_preset}
    return await client.get(f"/{entity_id}/insights", params=params)

async def get_placement_breakdown(
    entity_type: Annotated[str, Field(description="Type.")], 
    entity_id: Annotated[str, Field(description="The ID.")], 
    date_preset: Annotated[str, Field(description="Date.")] = "last_30d"
) -> dict:
    """Gets placement breakdown insights."""
    client = await MetaAPIClient.initialize()
    params = {"level": entity_type, "breakdowns": "publisher_platform,platform_position,device_platform", "date_preset": date_preset}
    return await client.get(f"/{entity_id}/insights", params=params)

async def get_hourly_breakdown(
    entity_type: Annotated[str, Field(description="Type.")], 
    entity_id: Annotated[str, Field(description="The ID.")], 
    date: Annotated[str, Field(description="Date string for breakdown.")], 
    timezone: Annotated[str, Field(description="advertiser or audience.")] = "advertiser"
) -> dict:
    """Gets hourly breakdown for a specific date."""
    client = await MetaAPIClient.initialize()
    tz_string = "hourly_stats_aggregated_by_advertiser_time_zone" if timezone == "advertiser" else "hourly_stats_aggregated_by_audience_time_zone"
    params = {"level": entity_type, "breakdowns": tz_string, "time_range": {"since": date, "until": date}}
    return await client.get(f"/{entity_id}/insights", params=params)

async def get_attribution_report(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    attribution_windows: Annotated[List[str], Field(description="E.g., ['28d_click', '1d_view'].")], 
    date_preset: Annotated[str, Field(description="Date.")] = "last_30d"
) -> dict:
    """Gets attribution window reports."""
    client = await MetaAPIClient.initialize()
    params = {
        "level": "account",
        "action_breakdowns": "action_type",
        "action_attribution_windows": attribution_windows,
        "date_preset": date_preset
    }
    return await client.get(f"/{ad_account_id}/insights", params=params)
