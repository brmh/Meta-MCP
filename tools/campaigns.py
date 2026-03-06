from typing import Optional, Literal, List, Annotated
from pydantic import Field
from fastmcp import FastMCP
from api.client import MetaAPIClient
from config.constants import Objective, Status

# This will be injected by the main server, but we can define the functions here
# For the decorator to work during registration we will apply them in server.py
# Or we can pass the initialized FastMCP object. Let's assume we decorate them in the module
# and import them to the server if `mcp` is shared.
# Actually, the best pattern for FastMCP is to define tools as async functions
# and the main app imports and decorates them, OR we define a tool registry.
# The prompt says: "@mcp.tool() decorator with complete natural-language description"
# So let's import the global `mcp` instance from server, or define a local one to export.
# Let's use a dummy router/registry or just define the functions and let `server.py` decorate them.
# The prompt implies `mcp` is imported from `server.py`, but `server.py` imports these modules.
# We will just define the functions and let `server.py` handle attaching them, or we create a global 
# mcp instance in a separate file (e.g. `mcp_server.py`) to avoid circular imports.

# To avoid circular imports, let's just create the functions and provide the exact
# signature and docstrings. `server.py` will import these and decorate them.
# Actually, wait, FastMCP can be passed around or imported. 

async def create_campaign(
    ad_account_id: Annotated[str, Field(
        description="The Meta ad account ID in format 'act_XXXXXXXXXX'. "
                    "Find this in Meta Ads Manager under Account Overview."
    )],
    name: Annotated[str, Field(
        description="Descriptive campaign name. Recommended format: "
                    "'Brand - Q1 2025 - Objective - Region' for easy management."
    )],
    objective: Annotated[Literal[
        "OUTCOME_AWARENESS", "OUTCOME_TRAFFIC", "OUTCOME_ENGAGEMENT",
        "OUTCOME_LEADS", "OUTCOME_APP_PROMOTION", "OUTCOME_SALES"
    ], Field(
        description="Campaign objective aligned to your goal: "
                    "OUTCOME_AWARENESS (brand visibility & recall), "
                    "OUTCOME_TRAFFIC (drive visits to website or app), "
                    "OUTCOME_ENGAGEMENT (maximize likes/comments/shares), "
                    "OUTCOME_LEADS (generate leads via forms or website), "
                    "OUTCOME_APP_PROMOTION (app installs & in-app events), "
                    "OUTCOME_SALES (drive purchases, catalog sales, ROAS)."
    )],
    status: Annotated[Literal["ACTIVE", "PAUSED"], Field(description="Initial status. PAUSED is recommended to build adsets and ads before going live.")] = "PAUSED",
    special_ad_categories: Annotated[List[str], Field(description="List of special ad categories (e.g., HOUSING, EMPLOYMENT, CREDIT, NONE). MUST be provided.")] = ["NONE"],
    daily_budget: Annotated[Optional[int], Field(description="Daily budget in account currency cents (e.g., 5000 for $50.00).")] = None,
    lifetime_budget: Annotated[Optional[int], Field(description="Lifetime budget in account currency cents.")] = None,
    bid_strategy: Annotated[Optional[str], Field(description="Optional bid strategy (e.g., LOWEST_COST_WITHOUT_CAP).")] = None,
    start_time: Annotated[Optional[str], Field(description="ISO 8601 start time.")] = None,
    stop_time: Annotated[Optional[str], Field(description="ISO 8601 stop time.")] = None,
    spend_cap: Annotated[Optional[int], Field(description="Spend cap in cents.")] = None,
    buying_type: Annotated[str, Field(description="Buying type (e.g., AUCTION, RESERVATION).")] = "AUCTION",
    is_skadnetwork_attribution: Annotated[bool, Field(description="Enable SKAdNetwork attribution for iOS 14+.")] = False,
    smart_promotion_type: Annotated[Optional[str], Field(description="Smart promotion type if applicable.")] = None
) -> dict:
    """
    Create a new Meta Ads campaign at the top level of the ads hierarchy.
    The campaign defines the advertising objective. All ad sets and ads
    within the campaign inherit this objective. Use PAUSED status when
    creating so you can configure ad sets and ads before going live.
    """
    client = await MetaAPIClient.initialize()
    
    payload = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": special_ad_categories,
        "buying_type": buying_type,
    }
    
    if daily_budget:
        payload["daily_budget"] = daily_budget
    if lifetime_budget:
        payload["lifetime_budget"] = lifetime_budget
    if bid_strategy:
        payload["bid_strategy"] = bid_strategy
    if start_time:
        payload["start_time"] = start_time
    if stop_time:
        payload["stop_time"] = stop_time
    if spend_cap:
        payload["spend_cap"] = spend_cap
    if is_skadnetwork_attribution:
        payload["is_skadnetwork_attribution"] = is_skadnetwork_attribution
    if smart_promotion_type:
        payload["smart_promotion_type"] = smart_promotion_type

    return await client.post(f"/{ad_account_id}/campaigns", data=payload)

async def get_campaign(
    campaign_id: Annotated[str, Field(description="The Campaign ID.")], 
    fields: Annotated[List[str], Field(description="List of fields to return (e.g., ['id', 'name', 'status', 'objective']).")] = ["id", "name", "status", "objective"]
) -> dict:
    """Gets details for a specific campaign."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{campaign_id}", params={"fields": fields})

async def list_campaigns(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    effective_status: Annotated[List[str], Field(description="Filter by statuses (e.g., ['ACTIVE', 'PAUSED']).")] = ["ACTIVE", "PAUSED"], 
    date_preset: Annotated[str, Field(description="Date preset (e.g., 'maximum', 'last_30d').")] = "maximum", 
    limit: Annotated[int, Field(description="Max results per page.")] = 25, 
    after: Annotated[Optional[str], Field(description="Pagination cursor.")] = None
) -> dict:
    """Lists campaigns in an ad account."""
    client = await MetaAPIClient.initialize()
    params = {
        "fields": "id,name,status,objective,effective_status",
        "effective_status": effective_status,
        "date_preset": date_preset,
        "limit": limit
    }
    if after:
        params["after"] = after
    return await client.get(f"/{ad_account_id}/campaigns", params=params)

async def update_campaign(
    campaign_id: Annotated[str, Field(description="The Campaign ID.")],
    name: Annotated[Optional[str], Field(description="New name.")] = None,
    status: Annotated[Optional[Literal["ACTIVE", "PAUSED", "DELETED", "ARCHIVED"]], Field(description="New status.")] = None,
    daily_budget: Annotated[Optional[int], Field(description="New daily budget in cents.")] = None,
    lifetime_budget: Annotated[Optional[int], Field(description="New lifetime budget in cents.")] = None,
    spend_cap: Annotated[Optional[int], Field(description="New spend cap in cents.")] = None 
) -> dict:
    """Updates an existing campaign."""
    client = await MetaAPIClient.initialize()
    payload = {}
    if name: payload["name"] = name
    if status: payload["status"] = status
    if daily_budget: payload["daily_budget"] = daily_budget
    if lifetime_budget: payload["lifetime_budget"] = lifetime_budget
    if spend_cap: payload["spend_cap"] = spend_cap
    
    return await client.post(f"/{campaign_id}", data=payload)

async def delete_campaign(
    campaign_id: Annotated[str, Field(description="The Campaign ID.")], 
    confirm: Annotated[bool, Field(description="Safety flag. Must be True to delete.")] = False
) -> dict:
    """Deletes a campaign. Requires confirm=True."""
    if not confirm:
        raise ValueError("You must pass confirm=True to delete a campaign.")
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{campaign_id}")

async def pause_campaign(campaign_id: Annotated[str, Field(description="The Campaign ID.")]) -> dict:
    """Pauses a campaign."""
    return await update_campaign(campaign_id=campaign_id, status="PAUSED")

async def resume_campaign(campaign_id: Annotated[str, Field(description="The Campaign ID.")]) -> dict:
    """Resumes a campaign."""
    return await update_campaign(campaign_id=campaign_id, status="ACTIVE")

async def duplicate_campaign(
    campaign_id: Annotated[str, Field(description="The Campaign ID.")], 
    new_name: Annotated[str, Field(description="Name for the new duplicate campaign.")], 
    status_after_copy: Annotated[str, Field(description="Status of new campaign (e.g., 'PAUSED').")] = "PAUSED", 
    deep_copy: Annotated[bool, Field(description="If True, copies adsets and ads too.")] = True, 
    replicate_destinations: Annotated[bool, Field(description="Replicate destinations where applicable.")] = True
) -> dict:
    """Duplicates a campaign."""
    client = await MetaAPIClient.initialize()
    payload = {
        "rename_options": {"rename_prefix": new_name},
        "status_option": status_after_copy,
        "deep_copy": deep_copy,
        "replicate_destinations": replicate_destinations
    }
    return await client.post(f"/{campaign_id}/copies", data=payload)
    
async def get_campaign_delivery_insights(campaign_id: Annotated[str, Field(description="The Campaign ID.")]) -> dict:
    """Gets quick delivery insights for a campaign."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{campaign_id}/insights", params={"date_preset": "last_30d"})

async def get_campaign_budget_schedules(campaign_id: Annotated[str, Field(description="The Campaign ID.")]) -> dict:
    """Gets budget schedules for a campaign."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{campaign_id}/adcampaign_schedules")

async def create_campaign_budget_schedule(
    campaign_id: Annotated[str, Field(description="The Campaign ID.")], 
    budget_schedules: Annotated[List[dict], Field(description="List of schedule options (e.g. {'budget_value': 1000, 'time_start': 16100000, 'time_end': 16109999}).")]
) -> dict:
    """Creates a budget schedule for a campaign."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{campaign_id}/budget_schedules", data={"budget_schedules": budget_schedules})
