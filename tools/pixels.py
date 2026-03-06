from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient
import time
import hashlib

def _hash_pii(data: str) -> str:
    if not data: return ""
    return hashlib.sha256(data.strip().lower().encode('utf-8')).hexdigest()

async def create_pixel(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    name: Annotated[str, Field(description="Name.")]
) -> dict:
    """Creates a pixel."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{ad_account_id}/adspixels", data={"name": name})

async def get_pixel(
    pixel_id: Annotated[str, Field(description="Pixel ID.")], 
    fields: Annotated[List[str], Field(description="Fields to return.")] = ["id", "name", "creation_time"]
) -> dict:
    """Gets pixel info."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{pixel_id}", params={"fields": fields})

async def list_pixels(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Lists pixels."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/adspixels", params={"fields": "id,name"})

async def update_pixel(pixel_id: Annotated[str, Field(description="Pixel ID.")], name: Annotated[str, Field(description="Name.")]) -> dict:
    """Updates pixel name."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{pixel_id}", data={"name": name})

async def get_pixel_stats(
    pixel_id: Annotated[str, Field(description="Pixel ID.")], 
    start_time: Annotated[int, Field(description="Unix start.")], 
    end_time: Annotated[int, Field(description="Unix end.")], 
    aggregation: Annotated[str, Field(description="Aggregation (e.g. event).")] = "event"
) -> dict:
    """Gets pixel stats."""
    client = await MetaAPIClient.initialize()
    params = {"start_time": start_time, "end_time": end_time, "aggregation": aggregation}
    return await client.get(f"/{pixel_id}/stats", params=params)

async def get_pixel_events(
    pixel_id: Annotated[str, Field(description="Pixel ID.")], 
    event: Annotated[Optional[str], Field(description="Event name filter (e.g. Purchase).")] = None, 
    since: Annotated[Optional[int], Field(description="Unix timestamp.")] = None
) -> dict:
    """Gets pixel events."""
    client = await MetaAPIClient.initialize()
    params = {}
    if event: params["event"] = event
    if since: params["since"] = since
    return await client.get(f"/{pixel_id}/events", params=params)

async def get_pixel_code(pixel_id: Annotated[str, Field(description="Pixel ID.")]) -> dict:
    """Gets the base pixel code snippet."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{pixel_id}", params={"fields": "code"})

# Conversions API (server-side events)
async def send_conversion_event(
    pixel_id: Annotated[str, Field(description="Pixel Dataset ID.")],
    events: Annotated[List[Dict[str, Any]], Field(description="List of event dicts.")],
    test_event_code: Annotated[Optional[str], Field(description="For testing.")] = None,
    partner_agent: Annotated[str, Field(description="Agent identifier.")] = "meta-ads-mcp"
) -> dict:
    """Sends server-side events via Conversions API."""
    client = await MetaAPIClient.initialize()
    
    # Hash PII fields explicitly
    for idx, event in enumerate(events):
        user_data = event.get("user_data", {})
        hashed_user_data = {}
        for k, v in user_data.items():
            if k in ["em", "ph", "ge", "db", "ln", "fn", "ct", "st", "zp", "country"]:
                if isinstance(v, list):
                    hashed_user_data[k] = [_hash_pii(item) for item in v]
                else:
                    hashed_user_data[k] = _hash_pii(str(v))
            else:
                 hashed_user_data[k] = v
        
        events[idx]["user_data"] = hashed_user_data
        
        # Ensure event_time is present
        if "event_time" not in events[idx]:
            events[idx]["event_time"] = int(time.time())

    payload = {"data": events, "partner_agent": partner_agent}
    if test_event_code: payload["test_event_code"] = test_event_code

    return await client.post(f"/{pixel_id}/events", data=payload)

async def test_conversion_event(
    pixel_id: Annotated[str, Field(description="Pixel ID.")], 
    events: Annotated[List[Dict[str, Any]], Field(description="List of events.")], 
    test_event_code: Annotated[str, Field(description="Test Event Code generated in Events Manager.")]
) -> dict:
    """Wrapper to force sending a conversion test event."""
    return await send_conversion_event(pixel_id, events, test_event_code=test_event_code)

async def get_conversion_event_log(
    pixel_id: Annotated[str, Field(description="Pixel ID.")], 
    since: Annotated[int, Field(description="Unix since.")], 
    until: Annotated[int, Field(description="Unix until.")], 
    test_event_code: Annotated[Optional[str], Field(description="Test event code.")] = None
) -> dict:
    """Gets a log of received Conversions API events."""
    client = await MetaAPIClient.initialize()
    params = {"since": since, "until": until}
    if test_event_code: params["test_event_code"] = test_event_code
    return await client.get(f"/{pixel_id}/receive_event_logs", params=params)

async def create_dataset(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    name: Annotated[str, Field(description="Dataset Name.")], 
    dataset_type: Annotated[str, Field(description="Type e.g., EVENT.")] = "EVENT"
) -> dict:
    """Creates a dataset (the newer pixel alternative)."""
    # Meta's Business id is typically needed for dataset creation directly
    # Assume ad_account logic, though structurally datasets belong to business Manager
    from config.settings import settings
    business_id = settings.META_BUSINESS_ID
    if not business_id:
        raise ValueError("META_BUSINESS_ID must be set to create datasets directly.")
        
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{business_id}/datasets", data={"name": name, "dataset_type": dataset_type})

async def list_datasets(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Lists datasets linked to an ad account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/datasets", params={"fields": "id,name"})
