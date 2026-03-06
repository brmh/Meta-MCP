from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

async def build_targeting_spec(
    countries: Annotated[List[str], Field(description="List of ISO country codes (e.g. ['US', 'GB']).")] = [],
    regions: Annotated[List[Dict[str, Any]], Field(description="List of region objects (e.g. [{'key': '3843'}]).")] = [],
    cities: Annotated[List[Dict[str, Any]], Field(description="List of city objects (e.g. [{'key': '2420605'}]).")] = [],
    zips: Annotated[List[Dict[str, Any]], Field(description="List of zip code objects.")] = [],
    location_types: Annotated[List[str], Field(description="home, recent, travel_in.")] = ["home", "recent"],
    excluded_geo_locations: Annotated[Dict[str, Any], Field(description="Same structure as geo_locations but for exclusion.")] = {},
    
    age_min: Annotated[int, Field(description="Minimum age (13-65).")] = 18,
    age_max: Annotated[int, Field(description="Maximum age (13-65).")] = 65,
    genders: Annotated[List[int], Field(description="1 for male, 2 for female. Empty for all.")] = [],
    
    interests: Annotated[List[Dict[str, Any]], Field(description="List of interest objects (e.g. [{'id': '123', 'name': 'Yoga'}]).")] = [],
    behaviors: Annotated[List[Dict[str, Any]], Field(description="List of behavior objects.")] = [],
    demographics: Annotated[List[Dict[str, Any]], Field(description="List of demographic objects.")] = [],
    life_events: Annotated[List[Dict[str, Any]], Field(description="List of life event objects.")] = [],
    industries: Annotated[List[Dict[str, Any]], Field(description="List of industry objects.")] = [],
    family_statuses: Annotated[List[Dict[str, Any]], Field(description="List of family status objects.")] = [],
    relationship_statuses: Annotated[List[int], Field(description="List of relationship status IDs.")] = [],
    education_statuses: Annotated[List[int], Field(description="List of education status IDs.")] = [],
    education_schools: Annotated[List[Dict[str, Any]], Field(description="List of school objects.")] = [],
    work_employers: Annotated[List[Dict[str, Any]], Field(description="List of employer objects.")] = [],
    work_positions: Annotated[List[Dict[str, Any]], Field(description="List of position objects.")] = [],
    income: Annotated[List[Dict[str, Any]], Field(description="List of income objects.")] = [],
    net_worth: Annotated[List[Dict[str, Any]], Field(description="List of net worth objects.")] = [],
    home_type: Annotated[List[Dict[str, Any]], Field(description="List of home type objects.")] = [],
    home_ownership: Annotated[List[Dict[str, Any]], Field(description="List of home ownership objects.")] = [],
    political_views: Annotated[List[int], Field(description="List of political view IDs.")] = [],
    generation: Annotated[List[Dict[str, Any]], Field(description="List of generation objects.")] = [],
    moms_of_children: Annotated[List[Dict[str, Any]], Field(description="List of moms of children objects.")] = [],
    ethnic_affinity: Annotated[List[Dict[str, Any]], Field(description="List of ethnic affinity objects.")] = [],
    
    custom_audiences: Annotated[List[Dict[str, Any]], Field(description="List of custom audience objects (e.g. [{'id': '123'}]).")] = [],
    excluded_custom_audiences: Annotated[List[Dict[str, Any]], Field(description="List of excluded custom audience objects.")] = [],
    flexible_spec: Annotated[List[Dict[str, Any]], Field(description="Flexible targeting spec for AND/OR logic.")] = [],
    exclusions: Annotated[Dict[str, Any], Field(description="Detailed exclusions spec.")] = {},
    
    publisher_platforms: Annotated[List[str], Field(description="E.g., facebook, instagram, audience_network, messenger.")] = [],
    facebook_positions: Annotated[List[str], Field(description="E.g., feed, right_hand_column, video_feeds.")] = [],
    instagram_positions: Annotated[List[str], Field(description="E.g., stream, story.")] = [],
    audience_network_positions: Annotated[List[str], Field(description="E.g., classic, instream_video.")] = [],
    messenger_positions: Annotated[List[str], Field(description="E.g., messenger_home.")] = [],
    device_platforms: Annotated[List[str], Field(description="E.g., mobile, desktop.")] = [],
    user_os: Annotated[List[str], Field(description="E.g., iOS, Android.")] = [],
    user_device: Annotated[List[str], Field(description="List of user device objects.")] = [],
    wireless_carrier: Annotated[List[str], Field(description="List of wireless carriers.")] = [],
    
    brand_safety_content_filter_levels: Annotated[List[str], Field(description="E.g., FACEBOOK_STANDARD, FACEBOOK_RELAXED, FACEBOOK_STRICT.")] = [],
    excluded_publisher_categories: Annotated[List[str], Field(description="List of excluded publisher categories.")] = [],
    excluded_publisher_list_ids: Annotated[List[str], Field(description="List of excluded publisher list IDs.")] = []
) -> dict:
    """Builds a validated targeting spec dictionary ready for the Meta API."""
    
    spec = {
        "age_min": age_min,
        "age_max": age_max,
        "location_types": location_types
    }
    
    geo_locations = {}
    if countries: geo_locations["countries"] = countries
    if regions: geo_locations["regions"] = regions
    if cities: geo_locations["cities"] = cities
    if zips: geo_locations["zips"] = zips
    if geo_locations: spec["geo_locations"] = geo_locations
    if excluded_geo_locations: spec["excluded_geo_locations"] = excluded_geo_locations
    if genders: spec["genders"] = genders

    if interests: spec["interests"] = interests
    if behaviors: spec["behaviors"] = behaviors
    if demographics: spec["demographics"] = demographics
    if life_events: spec["life_events"] = life_events
    if industries: spec["industries"] = industries
    if family_statuses: spec["family_statuses"] = family_statuses
    if relationship_statuses: spec["relationship_statuses"] = relationship_statuses
    if education_statuses: spec["education_statuses"] = education_statuses
    if education_schools: spec["education_schools"] = education_schools
    if work_employers: spec["work_employers"] = work_employers
    if work_positions: spec["work_positions"] = work_positions
    if income: spec["income"] = income
    if net_worth: spec["net_worth"] = net_worth
    if home_type: spec["home_type"] = home_type
    if home_ownership: spec["home_ownership"] = home_ownership
    if political_views: spec["political_views"] = political_views
    if generation: spec["generation"] = generation
    if moms_of_children: spec["moms_of_children"] = moms_of_children
    if ethnic_affinity: spec["ethnic_affinity"] = ethnic_affinity

    if custom_audiences: spec["custom_audiences"] = custom_audiences
    if excluded_custom_audiences: spec["excluded_custom_audiences"] = excluded_custom_audiences
    if flexible_spec: spec["flexible_spec"] = flexible_spec
    if exclusions: spec["exclusions"] = exclusions

    if publisher_platforms: spec["publisher_platforms"] = publisher_platforms
    if facebook_positions: spec["facebook_positions"] = facebook_positions
    if instagram_positions: spec["instagram_positions"] = instagram_positions
    if audience_network_positions: spec["audience_network_positions"] = audience_network_positions
    if messenger_positions: spec["messenger_positions"] = messenger_positions
    if device_platforms: spec["device_platforms"] = device_platforms
    if user_os: spec["user_os"] = user_os
    if user_device: spec["user_device"] = user_device
    if wireless_carrier: spec["wireless_carrier"] = wireless_carrier

    if brand_safety_content_filter_levels: spec["brand_safety_content_filter_levels"] = brand_safety_content_filter_levels
    if excluded_publisher_categories: spec["excluded_publisher_categories"] = excluded_publisher_categories
    if excluded_publisher_list_ids: spec["excluded_publisher_list_ids"] = excluded_publisher_list_ids

    return spec

async def create_adset(
    campaign_id: Annotated[str, Field(description="The parent Campaign ID.")],
    name: Annotated[str, Field(description="Ad set name.")],
    status: Annotated[str, Field(description="E.g., ACTIVE, PAUSED.")],
    optimization_goal: Annotated[str, Field(description="E.g., REACH, LINK_CLICKS, OFFSITE_CONVERSIONS.")],
    billing_event: Annotated[str, Field(description="E.g., IMPRESSIONS, LINK_CLICKS.")],
    daily_budget: Annotated[Optional[int], Field(description="Daily budget in cents.")] = None,
    lifetime_budget: Annotated[Optional[int], Field(description="Lifetime budget in cents.")] = None,
    bid_amount: Annotated[Optional[int], Field(description="Manual bid amount in cents.")] = None,
    bid_strategy: Annotated[Optional[str], Field(description="E.g., LOWEST_COST_WITHOUT_CAP, COST_CAP.")] = None,
    targeting: Annotated[Dict[str, Any], Field(description="Targeting spec generated by build_targeting_spec.")] = {},
    start_time: Annotated[Optional[str], Field(description="ISO 8601 start time.")] = None,
    end_time: Annotated[Optional[str], Field(description="ISO 8601 end time.")] = None,
    attribution_spec: Annotated[Optional[List[Dict[str, Any]]], Field(description="Attribution window spec.")] = None,
    destination_type: Annotated[Optional[str], Field(description="E.g., WEBSITE, MESSENGER.")] = None,
    promoted_object: Annotated[Optional[Dict[str, Any]], Field(description="What is being promoted (e.g., pixel id, page id).")] = None,
    pacing_type: Annotated[List[str], Field(description="E.g., ['standard'] or ['no_pacing'].")] = ["standard"],
    frequency_control_specs: Annotated[Optional[List[Dict[str, Any]]], Field(description="Frequency rules.")] = None,
    is_dynamic_creative: Annotated[bool, Field(description="Whether to use dynamic creative.")] = False
) -> dict:
    """"Creates a new ad set within a campaign."""
    client = await MetaAPIClient.initialize()
    payload = {
        "campaign_id": campaign_id,
        "name": name,
        "status": status,
        "optimization_goal": optimization_goal,
        "billing_event": billing_event,
        "targeting": targeting,
        "pacing_type": pacing_type,
        "is_dynamic_creative": is_dynamic_creative
    }
    
    if daily_budget: payload["daily_budget"] = daily_budget
    if lifetime_budget: payload["lifetime_budget"] = lifetime_budget
    if bid_amount: payload["bid_amount"] = bid_amount
    if bid_strategy: payload["bid_strategy"] = bid_strategy
    if start_time: payload["start_time"] = start_time
    if end_time: payload["end_time"] = end_time
    if attribution_spec: payload["attribution_spec"] = attribution_spec
    if destination_type: payload["destination_type"] = destination_type
    if promoted_object: payload["promoted_object"] = promoted_object
    if frequency_control_specs: payload["frequency_control_specs"] = frequency_control_specs

    # Extract ad_account_id from campaign to create adset
    campaign = await client.get(f"/{campaign_id}", params={"fields": "account_id"})
    ad_account_id = f"act_{campaign['account_id']}"
    
    return await client.post(f"/{ad_account_id}/adsets", data=payload)

async def get_adset(
    adset_id: Annotated[str, Field(description="The Ad Set ID.")], 
    fields: Annotated[List[str], Field(description="List of fields to return.")] = ["id", "name", "status"]
) -> dict:
    """"Gets an ad set by ID."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{adset_id}", params={"fields": fields})

async def list_adsets(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    campaign_id: Annotated[Optional[str], Field(description="Filter by Campaign ID.")] = None, 
    effective_status: Annotated[List[str], Field(description="Filter by effective status.")] = ["ACTIVE", "PAUSED"], 
    limit: Annotated[int, Field(description="Max results.")] = 25, 
    after: Annotated[Optional[str], Field(description="Pagination cursor.")] = None
) -> dict:
    """Lists ad sets in an account or campaign."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "id,name,status,campaign_id", "effective_status": effective_status, "limit": limit}
    if after: params["after"] = after
    
    endpoint = f"/{campaign_id}/adsets" if campaign_id else f"/{ad_account_id}/adsets"
    return await client.get(endpoint, params=params)

async def update_adset(
    adset_id: Annotated[str, Field(description="The Ad Set ID.")], 
    name: Annotated[Optional[str], Field(description="New name.")] = None, 
    status: Annotated[Optional[str], Field(description="New status.")] = None, 
    daily_budget: Annotated[Optional[int], Field(description="New daily budget.")] = None, 
    targeting: Annotated[Optional[Dict[str, Any]], Field(description="New targeting spec.")] = None
) -> dict:
    """Updates an existing ad set."""
    client = await MetaAPIClient.initialize()
    payload = {}
    if name: payload["name"] = name
    if status: payload["status"] = status
    if daily_budget: payload["daily_budget"] = daily_budget
    if targeting: payload["targeting"] = targeting
    
    return await client.post(f"/{adset_id}", data=payload)

async def delete_adset(
    adset_id: Annotated[str, Field(description="The Ad Set ID.")], 
    confirm: Annotated[bool, Field(description="Safety flag to confirm deletion.")] = False
) -> dict:
    """Deletes an ad set."""
    if not confirm:
        raise ValueError("confirm=True is required to delete.")
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{adset_id}")

async def pause_adset(adset_id: Annotated[str, Field(description="The Ad Set ID.")]) -> dict:
    """Pauses an ad set."""
    return await update_adset(adset_id=adset_id, status="PAUSED")

async def resume_adset(adset_id: Annotated[str, Field(description="The Ad Set ID.")]) -> dict:
    """Resumes an ad set."""
    return await update_adset(adset_id=adset_id, status="ACTIVE")

async def duplicate_adset(
    adset_id: Annotated[str, Field(description="The Ad Set ID to duplicate.")], 
    campaign_id: Annotated[Optional[str], Field(description="Campaign ID to duplicate into. If empty, duplicates into original campaign.")] = None, 
    new_name: Annotated[Optional[str], Field(description="Prefix for the new Ad Set name.")] = None
) -> dict:
    """Duplicates an ad set."""
    client = await MetaAPIClient.initialize()
    payload = {"deep_copy": True}
    if campaign_id: payload["campaign_id"] = campaign_id
    if new_name: payload["rename_options"] = {"rename_prefix": new_name}
    
    return await client.post(f"/{adset_id}/copies", data=payload)

async def get_adset_delivery_estimate(
    adset_id: Annotated[str, Field(description="The Ad Set ID.")], 
    optimization_goal: Annotated[str, Field(description="The optimization goal (e.g. REACH).")], 
    targeting_spec: Annotated[Dict[str, Any], Field(description="The updated targeting spec dict.")]
) -> dict:
    """Gets delivery estimate for an ad set."""
    client = await MetaAPIClient.initialize()
    params = {
        "optimization_goal": optimization_goal,
        "targeting_spec": targeting_spec
    }
    return await client.get(f"/{adset_id}/delivery_estimate", params=params)

async def search_targeting_interests(
    q: Annotated[str, Field(description="Query string for the interest (e.g., 'Yoga').")], 
    limit: Annotated[int, Field(description="Max results.")] = 20
) -> dict:
    """Searches for targeting interests based on a query."""
    client = await MetaAPIClient.initialize()
    return await client.get("/search", params={"type": "adinterest", "q": q, "limit": limit})

async def search_targeting_behaviors(
    q: Annotated[str, Field(description="Query string for behaviors.")], 
    limit: Annotated[int, Field(description="Max results.")] = 20
) -> dict:
    """Searches for targeting behaviors."""
    client = await MetaAPIClient.initialize()
    return await client.get("/search", params={"type": "adTargetingCategory", "class": "behaviors", "q": q, "limit": limit})

async def browse_targeting_categories(
    type: Annotated[str, Field(description="Category type (e.g., adTargetingCategory).")], 
    class_id: Annotated[Optional[str], Field(description="Specific class ID (e.g., interests, behaviors).")] = None
) -> dict:
    """Browses broad targeting categories."""
    client = await MetaAPIClient.initialize()
    params = {"type": type}
    if class_id:
        params["class"] = class_id
    return await client.get("/search", params=params)

async def get_reach_estimate(
    ad_account_id: Annotated[str, Field(description="The Ad Account ID.")], 
    targeting_spec: Annotated[Dict[str, Any], Field(description="Targeting spec generated by build_targeting_spec.")], 
    optimization_goal: Annotated[str, Field(description="E.g., REACH, LINK_CLICKS.")], 
    promoted_object: Annotated[Dict[str, Any], Field(description="What is being promoted.")], 
    currency: Annotated[str, Field(description="Account currency (e.g., USD).")]
) -> dict:
    """Gets a reach estimate for a brand new targeting definition."""
    client = await MetaAPIClient.initialize()
    params = {
        "targeting_spec": targeting_spec,
        "optimization_goal": optimization_goal,
        "promoted_object": promoted_object,
        "currency": currency
    }
    return await client.get(f"/{ad_account_id}/delivery_estimate", params=params)
