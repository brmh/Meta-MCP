from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

async def create_ad(
    adset_id: Annotated[str, Field(description="The parent Ad Set ID.")],
    name: Annotated[str, Field(description="Ad name.")],
    creative: Annotated[Dict[str, Any], Field(description="Creative dictionary (should contain creative_id).")],
    status: Annotated[str, Field(description="Status (e.g., ACTIVE, PAUSED).")] = "PAUSED",
    tracking_specs: Annotated[Optional[List[Dict[str, Any]]], Field(description="URL tag tracking specs.")] = None,
    conversion_domain: Annotated[Optional[str], Field(description="Domain to track conversions on.")] = None,
    display_sequence: Annotated[Optional[int], Field(description="Display sequence for multi-ad ordering.")] = None,
    engagement_audience: Annotated[bool, Field(description="Include in engagement audiences.")] = False,
    priority: Annotated[Optional[int], Field(description="Priority of the ad.")] = None
) -> dict:
    """Creates a new ad."""
    client = await MetaAPIClient.initialize()
    payload = {
        "adset_id": adset_id,
        "name": name,
        "creative": creative,
        "status": status,
        "engagement_audience": engagement_audience
    }
    
    if tracking_specs: payload["tracking_specs"] = tracking_specs
    if conversion_domain: payload["conversion_domain"] = conversion_domain
    if display_sequence is not None: payload["display_sequence"] = display_sequence
    if priority is not None: payload["priority"] = priority

    # Extract ad_account_id from adset
    adset = await client.get(f"/{adset_id}", params={"fields": "account_id"})
    ad_account_id = f"act_{adset['account_id']}"
    
    return await client.post(f"/{ad_account_id}/ads", data=payload)

async def get_ad(
    ad_id: Annotated[str, Field(description="The Ad ID.")], 
    fields: Annotated[List[str], Field(description="Fields to return.")] = ["id", "name", "status"]
) -> dict:
    """Gets an ad by ID."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_id}", params={"fields": fields})

async def list_ads(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    campaign_id: Annotated[Optional[str], Field(description="Filter by Campaign ID.")] = None, 
    adset_id: Annotated[Optional[str], Field(description="Filter by Ad Set ID.")] = None, 
    effective_status: Annotated[List[str], Field(description="Filter by effective status.")] = ["ACTIVE", "PAUSED"], 
    limit: Annotated[int, Field(description="Max results.")] = 25, 
    after: Annotated[Optional[str], Field(description="Pagination cursor.")] = None
) -> dict:
    """Lists ads in an account, campaign, or ad set."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "id,name,status,adset_id,campaign_id", "effective_status": effective_status, "limit": limit}
    if after: params["after"] = after
    
    endpoint = f"/{ad_account_id}/ads"
    if adset_id: endpoint = f"/{adset_id}/ads"
    elif campaign_id: endpoint = f"/{campaign_id}/ads"
    
    return await client.get(endpoint, params=params)

async def update_ad(
    ad_id: Annotated[str, Field(description="The Ad ID.")],
    name: Annotated[Optional[str], Field(description="New name.")] = None,
    status: Annotated[Optional[str], Field(description="New status.")] = None,
    creative: Annotated[Optional[Dict[str, Any]], Field(description="New creative dictonary.")] = None
) -> dict:
    """Updates an existing ad."""
    client = await MetaAPIClient.initialize()
    payload = {}
    if name: payload["name"] = name
    if status: payload["status"] = status
    if creative: payload["creative"] = creative
    
    return await client.post(f"/{ad_id}", data=payload)

async def delete_ad(ad_id: Annotated[str, Field(description="The Ad ID.")], confirm: Annotated[bool, Field(description="Safety flag.")] = False) -> dict:
    """Deletes an ad."""
    if not confirm:
        raise ValueError("confirm=True is required to delete.")
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{ad_id}")

async def pause_ad(ad_id: Annotated[str, Field(description="The Ad ID.")]) -> dict:
    """Pauses an ad."""
    return await update_ad(ad_id=ad_id, status="PAUSED")

async def resume_ad(ad_id: Annotated[str, Field(description="The Ad ID.")]) -> dict:
    """Resumes an ad."""
    return await update_ad(ad_id=ad_id, status="ACTIVE")

async def duplicate_ad(
    ad_id: Annotated[str, Field(description="The Ad ID.")], 
    adset_id: Annotated[Optional[str], Field(description="Ad Set to duplicate into.")] = None, 
    new_name: Annotated[Optional[str], Field(description="New name prefix.")] = None
) -> dict:
    """Duplicates an ad."""
    client = await MetaAPIClient.initialize()
    payload = {}
    if adset_id: payload["adset_id"] = adset_id
    if new_name: payload["rename_options"] = {"rename_prefix": new_name}
    
    return await client.post(f"/{ad_id}/copies", data=payload)

async def get_ad_preview(
    ad_id: Annotated[str, Field(description="The Ad ID.")],
    ad_format: Annotated[Literal[
        "DESKTOP_FEED_STANDARD", "MOBILE_FEED_STANDARD",
        "MOBILE_FEED_BASIC", "MOBILE_INTERSTITIAL",
        "INSTAGRAM_STANDARD", "INSTAGRAM_EXPLORE",
        "INSTAGRAM_STORY", "FACEBOOK_STORY",
        "MESSENGER_MOBILE_INBOX_MEDIA", "AUDIENCE_NETWORK_OUTSTREAM_VIDEO",
        "RIGHT_COLUMN_STANDARD", "MARKETPLACE_MOBILE"
    ], Field(description="The format (placement) of the preview.")]
) -> dict:
    """Gets an iframe preview HTML of a saved ad."""
    client = await MetaAPIClient.initialize()
    params = {"ad_format": ad_format}
    return await client.get(f"/{ad_id}/previews", params=params)

async def get_ad_preview_from_spec(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    creative_spec: Annotated[Dict[str, Any], Field(description="Mock creative dictionary.")], 
    ad_format: Annotated[str, Field(description="The format of the preview.")]
) -> dict:
    """Gets a preview of an ad directly from a creative spec (without creating the ad)."""
    client = await MetaAPIClient.initialize()
    params = {"creative": creative_spec, "ad_format": ad_format}
    return await client.get(f"/{ad_account_id}/generatepreviews", params=params)

async def create_ad_label(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    name: Annotated[str, Field(description="Name of the label.")]
) -> dict:
    """Creates a new ad label (tag) on the ad account."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{ad_account_id}/adlabels", data={"name": name})

async def list_ad_labels(ad_account_id: Annotated[str, Field(description="The Ad Account ID.")]) -> dict:
    """Lists ad labels on an account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/adlabels", params={"fields": "id,name"})

async def get_ad_activity_history(
    ad_id: Annotated[str, Field(description="The Ad ID.")], 
    since: Annotated[Optional[str], Field(description="Start time (Unix timestamp).")] = None, 
    until: Annotated[Optional[str], Field(description="End time (Unix timestamp).")] = None
) -> dict:
    """Gets the change history of an ad."""
    client = await MetaAPIClient.initialize()
    params = {}
    if since: params["since"] = since
    if until: params["until"] = until
    return await client.get(f"/{ad_id}/activities", params=params)

async def validate_ad(ad_id: Annotated[str, Field(description="The Ad ID.")]) -> dict:
    """Validates an ad's delivery capability based on current policies and targeting."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "delivery_info,status"}
    return await client.get(f"/{ad_id}", params=params)
