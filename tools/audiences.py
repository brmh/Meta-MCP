import hashlib
from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

def _hash_data(data: str) -> str:
    return hashlib.sha256(data.strip().lower().encode('utf-8')).hexdigest()

async def create_customer_list_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    name: Annotated[str, Field(description="Audience name.")],
    description: Annotated[str, Field(description="Audience description.")],
    customer_file_source: Annotated[Literal[
        "USER_PROVIDED_ONLY", "PARTNER_PROVIDED_ONLY",
        "BOTH_USER_AND_PARTNER_PROVIDED"
    ], Field(description="Source of the data.")]
) -> dict:
    """"Creates a custom audience container for customer lists."""
    client = await MetaAPIClient.initialize()
    payload = {
        "name": name,
        "description": description,
        "subtype": "CUSTOM",
        "customer_file_source": customer_file_source
    }
    return await client.post(f"/{ad_account_id}/customaudiences", data=payload)

async def add_users_to_audience(
    audience_id: Annotated[str, Field(description="Audience ID.")],
    schema: Annotated[List[str], Field(description="List of fields (e.g. ['EMAIL', 'PHONE']).")],
    data: Annotated[List[List[str]], Field(description="Array of user data arrays.")],
    is_raw: Annotated[bool, Field(description="If true, server hashes the data before sending.")] = True
) -> dict:
    """"Adds users to a customer list custom audience."""
    # Hash data locally if it's raw
    if is_raw:
        processed_data = [[_hash_data(str(item)) for item in row] for row in data]
    else:
        processed_data = data
        
    client = await MetaAPIClient.initialize()
    payload = {
        "payload": {
            "schema": schema,
            "data": processed_data
        }
    }
    return await client.post(f"/{audience_id}/users", data=payload)

async def remove_users_from_audience(
    audience_id: Annotated[str, Field(description="Audience ID.")], 
    schema: Annotated[List[str], Field(description="Schema fields.")], 
    data: Annotated[List[List[str]], Field(description="User data arrays.")]
) -> dict:
    """Removes users from a custom audience."""
    # Automatically hashing
    processed_data = [[_hash_data(str(item)) for item in row] for row in data]
    client = await MetaAPIClient.initialize()
    payload = {
        "payload": {
            "schema": schema,
            "data": processed_data
        }
    }
    return await client.delete(f"/{audience_id}/users", params=payload)

async def create_website_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    name: Annotated[str, Field(description="Audience Name.")],
    description: Annotated[str, Field(description="Description.")],
    pixel_id: Annotated[str, Field(description="Pixel ID.")],
    retention_days: Annotated[int, Field(description="Number of days (1-180).")],
    rule: Annotated[Dict[str, Any], Field(description="JSON rules for website traffic.")]
) -> dict:
    """Creates a website traffic custom audience."""
    client = await MetaAPIClient.initialize()
    payload = {
        "name": name,
        "description": description,
        "pixel_id": pixel_id,
        "retention_days": retention_days,
        "rule": rule,
        "subtype": "WEBSITE",
        "prefill": True
    }
    return await client.post(f"/{ad_account_id}/customaudiences", data=payload)

async def create_app_activity_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    name: Annotated[str, Field(description="Audience name.")],
    description: Annotated[str, Field(description="Description.")],
    app_id: Annotated[str, Field(description="App ID.")],
    retention_days: Annotated[int, Field(description="Retention days.")],
    rule: Annotated[Dict[str, Any], Field(description="Rules for app activity.")]
) -> dict:
    """Creates an app activity custom audience."""
    client = await MetaAPIClient.initialize()
    payload = {
        "name": name,
        "description": description,
        "subtype": "APP",
        "retention_days": retention_days,
        "rule": rule,
        "prefill": True
    }
    # App id implicitly part of the context or requires specific object binding, usually app_id isn't directly passed here if not in rules
    return await client.post(f"/{ad_account_id}/customaudiences", data=payload)

async def create_engagement_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    name: Annotated[str, Field(description="Name.")],
    description: Annotated[str, Field(description="Description.")],
    retention_days: Annotated[int, Field(description="Retention days.")],
    event_sources: Annotated[List[Dict[str, Any]], Field(description="Event sources (e.g., page, ig account).")],
    inclusions: Annotated[List[Dict[str, Any]], Field(description="Inclusion rules.")],
    exclusions: Annotated[List[Dict[str, Any]], Field(description="Exclusion rules.")]
) -> dict:
    """Creates an engagement custom audience."""
    client = await MetaAPIClient.initialize()
    rule = {
        "inclusions": inclusions,
        "exclusions": exclusions
    }
    payload = {
        "name": name,
        "description": description,
        "subtype": "ENGAGEMENT",
        "retention_days": retention_days,
        "rule": rule,
        "event_sources": event_sources,
        "prefill": True
    }
    return await client.post(f"/{ad_account_id}/customaudiences", data=payload)

async def create_lookalike_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    name: Annotated[str, Field(description="Name.")],
    origin_audience_id: Annotated[str, Field(description="Source Audience ID.")],
    country: Annotated[str, Field(description="Country Code (e.g. US).")],
    ratio: Annotated[float, Field(description="Ratio (0.01 to 0.20).")] = 0.01,
    lookalike_type: Annotated[str, Field(description="Type: similarity, reach.")] = "similarity"
) -> dict:
    """Creates a lookalike audience."""
    client = await MetaAPIClient.initialize()
    payload = {
        "name": name,
        "subtype": "LOOKALIKE",
        "origin_audience_id": origin_audience_id,
        "lookalike_spec": {
            "country": country,
            "ratio": ratio,
            "type": lookalike_type
        }
    }
    return await client.post(f"/{ad_account_id}/customaudiences", data=payload)

async def get_audience(
    audience_id: Annotated[str, Field(description="Audience ID.")], 
    fields: Annotated[List[str], Field(description="Fields to return.")] = ["id", "name", "approximate_count_upper_bound"]
) -> dict:
    """Gets audience details."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{audience_id}", params={"fields": fields})

async def list_audiences(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    limit: Annotated[int, Field(description="Results per page.")] = 25, 
    after: Annotated[Optional[str], Field(description="Cursor.")] = None
) -> dict:
    """Lists custom audiences."""
    client = await MetaAPIClient.initialize()
    params = {"limit": limit, "fields": "id,name,subtype"}
    if after: params["after"] = after
    return await client.get(f"/{ad_account_id}/customaudiences", params=params)

async def update_audience(
    audience_id: Annotated[str, Field(description="Audience ID.")], 
    name: Annotated[str, Field(description="New name.")], 
    description: Annotated[str, Field(description="New description.")], 
    retention_days: Annotated[Optional[int], Field(description="New retention days.")] = None
) -> dict:
    """Updates custom audience."""
    client = await MetaAPIClient.initialize()
    payload = {"name": name, "description": description}
    if retention_days: payload["retention_days"] = retention_days
    return await client.post(f"/{audience_id}", data=payload)

async def delete_audience(audience_id: Annotated[str, Field(description="Audience ID.")], confirm: Annotated[bool, Field(description="Confirm flag.")] = False) -> dict:
    """Deletes custom audience."""
    if not confirm:
        raise ValueError("confirm=True is required.")
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{audience_id}")

async def share_audience(
    audience_id: Annotated[str, Field(description="Audience ID.")], 
    ad_account_ids: Annotated[List[str], Field(description="List of ad accounts to share with.")]
) -> dict:
    """Shares an audience wth other accounts."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{audience_id}/share_account_to_adaccounts", data={"adaccounts": ad_account_ids})

async def get_audience_size_estimate(audience_id: Annotated[str, Field(description="Audience ID.")]) -> dict:
    """Gets approximate size of custom audience."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{audience_id}", params={"fields": "approximate_count_upper_bound,approximate_count_lower_bound"})

async def get_audience_activity(audience_id: Annotated[str, Field(description="Audience ID.")]) -> dict:
    """Gets activity/history for an audience."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{audience_id}/activities")

async def create_saved_audience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    name: Annotated[str, Field(description="Audience Name.")], 
    description: Annotated[str, Field(description="Audience Description.")], 
    targeting: Annotated[Dict[str, Any], Field(description="Targeting Dict.")]
) -> dict:
    """Creates a saved audience (Core audience)."""
    client = await MetaAPIClient.initialize()
    payload = {"name": name, "description": description, "targeting": targeting}
    return await client.post(f"/{ad_account_id}/saved_audiences", data=payload)

async def list_saved_audiences(ad_account_id: Annotated[str, Field(description="Ad Account ID.")], limit: Annotated[int] = 25) -> dict:
    """Lists saved audiences."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/saved_audiences", params={"limit": limit, "fields": "id,name"})

async def delete_saved_audience(audience_id: Annotated[str, Field(description="Audience ID.")]) -> dict:
    """Deletes a saved audience."""
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{audience_id}")
