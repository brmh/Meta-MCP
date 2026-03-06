import os
from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient
import httpx

async def create_image_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Name of the creative.")],
    link_url: Annotated[str, Field(description="Destinatio URL.")],
    image_hash: Annotated[Optional[str], Field(description="Hash of an already uploaded image.")] = None,
    image_url: Annotated[Optional[str], Field(description="URL of an image to use.")] = None,
    title: Annotated[Optional[str], Field(description="Headline.")] = None,
    body: Annotated[Optional[str], Field(description="Primary text.")] = None,
    display_url: Annotated[Optional[str], Field(description="Display block text.")] = None,
    call_to_action: Annotated[Optional[Dict[str, Any]], Field(description="E.g., {'type': 'LEARN_MORE', 'value': {'link': '...'}}")] = None,
    instagram_actor_id: Annotated[Optional[str], Field(description="Instagram account ID.")] = None,
    url_tags: Annotated[Optional[str], Field(description="URL tracking tags.")] = None,
    link_og_id: Annotated[Optional[str], Field(description="Open Graph Object ID.")] = None
) -> dict:
    """"Creates a standard image ad creative."""
    client = await MetaAPIClient.initialize()
    
    link_data = {"link": link_url}
    if image_hash: link_data["image_hash"] = image_hash
    elif image_url: link_data["picture"] = image_url
    if title: link_data["name"] = title
    if body: link_data["message"] = body
    if display_url: link_data["caption"] = display_url
    if call_to_action: link_data["call_to_action"] = call_to_action
    
    object_story_spec = {
        "page_id": page_id,
        "link_data": link_data
    }
    if instagram_actor_id: object_story_spec["instagram_actor_id"] = instagram_actor_id
    
    payload = {
        "name": name,
        "object_story_spec": object_story_spec
    }
    if url_tags: payload["url_tags"] = url_tags
    if body: payload["body"] = body # duplicate sometimes needed
    if title: payload["title"] = title
        
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def create_video_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Creative name.")],
    video_id: Annotated[str, Field(description="Uploaded video ID.")],
    link_url: Annotated[str, Field(description="Destination URL.")],
    title: Annotated[Optional[str], Field(description="Headline.")] = None,
    message: Annotated[Optional[str], Field(description="Primary text.")] = None,
    call_to_action: Annotated[Optional[Dict[str, Any]], Field(description="CTA dictionary.")] = None,
    thumbnail_url: Annotated[Optional[str], Field(description="URL for thumbnail.")] = None,
    instagram_actor_id: Annotated[Optional[str], Field(description="IG specific actor.")] = None,
    url_tags: Annotated[Optional[str], Field(description="Tracking tags.")] = None
) -> dict:
    """Creates a video ad creative."""
    client = await MetaAPIClient.initialize()
    
    video_data = {
        "video_id": video_id,
        "call_to_action": call_to_action or {"type": "LEARN_MORE", "value": {"link": link_url}}
    }
    if title: video_data["title"] = title
    if message: video_data["message"] = message
    if thumbnail_url: video_data["image_url"] = thumbnail_url
    
    object_story_spec = {
        "page_id": page_id,
        "video_data": video_data
    }
    if instagram_actor_id: object_story_spec["instagram_actor_id"] = instagram_actor_id
    
    payload = {
        "name": name,
        "object_story_spec": object_story_spec
    }
    if url_tags: payload["url_tags"] = url_tags
    
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def create_carousel_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Name.")],
    link: Annotated[str, Field(description="Fallback link.")],
    child_attachments: Annotated[List[Dict[str, Any]], Field(description="List of cards. [{image_hash, link, name, description, call_to_action}]")],
    message: Annotated[Optional[str], Field(description="Primary text above carousel.")] = None,
    multi_share_optimized: Annotated[bool, Field(description="Automatically show best cards first.")] = True,
    multi_share_end_card: Annotated[bool, Field(description="Show page profile card at end.")] = True,
    call_to_action: Annotated[Optional[Dict[str, Any]], Field(description="Default CTA if not per-card.")] = None,
    instagram_actor_id: Annotated[Optional[str], Field(description="IG specific actor.")] = None
) -> dict:
    """Creates a carousel creative."""
    client = await MetaAPIClient.initialize()
    
    link_data = {
        "link": link,
        "child_attachments": child_attachments,
        "multi_share_optimized": multi_share_optimized,
        "multi_share_end_card": multi_share_end_card
    }
    if message: link_data["message"] = message
    if call_to_action: link_data["call_to_action"] = call_to_action
    
    object_story_spec = {
        "page_id": page_id,
        "link_data": link_data
    }
    if instagram_actor_id: object_story_spec["instagram_actor_id"] = instagram_actor_id
    
    payload = {
        "name": name,
        "object_story_spec": object_story_spec
    }
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def create_collection_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Name.")],
    link: Annotated[str, Field(description="Instant experience URL.")],
    template_data: Annotated[Dict[str, Any], Field(description="Collection template data.")],
    message: Annotated[Optional[str], Field(description="Primary text.")] = None,
    instagram_actor_id: Annotated[Optional[str], Field(description="IG specific actor.")] = None
) -> dict:
    """Creates a collection creative."""
    client = await MetaAPIClient.initialize()
    
    template_data_wrapper = {
        "link": link,
        "template_data": template_data
    }
    if message: template_data_wrapper["message"] = message
    
    object_story_spec = {
        "page_id": page_id,
        "template_data": template_data_wrapper
    }
    if instagram_actor_id: object_story_spec["instagram_actor_id"] = instagram_actor_id
    
    payload = {
        "name": name,
        "object_story_spec": object_story_spec
    }
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def create_dynamic_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Name.")],
    asset_feed_spec: Annotated[Dict[str, Any], Field(description="Asset feed covering images, titles, bodies, descriptions, link_urls, call_to_action_types.")],
    call_to_action: Annotated[Optional[Dict[str, Any]], Field(description="Fallback CTA.")] = None,
    instagram_actor_id: Annotated[Optional[str], Field(description="IG specific actor.")] = None
) -> dict:
    """Creates a dynamic ad creative."""
    client = await MetaAPIClient.initialize()
    
    payload = {
        "name": name,
        "asset_feed_spec": asset_feed_spec,
        "object_story_spec": {"page_id": page_id}
    }
    if instagram_actor_id: payload["object_story_spec"]["instagram_actor_id"] = instagram_actor_id
    
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def create_stories_creative(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")],
    page_id: Annotated[str, Field(description="Facebook Page ID.")],
    name: Annotated[str, Field(description="Name.")],
    link_url: Annotated[str, Field(description="Swipe up link.")],
    video_id: Annotated[Optional[str], Field(description="Video ID.")] = None,
    image_hash: Annotated[Optional[str], Field(description="Image Hash.")] = None,
    call_to_action: Annotated[Optional[Dict[str, Any]], Field(description="CTA details.")] = None
) -> dict:
    """Creates a story-specific creative."""
    client = await MetaAPIClient.initialize()
    
    spec = {"page_id": page_id}
    if video_id:
         spec["video_data"] = {
             "video_id": video_id,
             "call_to_action": call_to_action or {"type": "LEARN_MORE", "value": {"link": link_url}}
         }
    elif image_hash:
         spec["link_data"] = {
             "link": link_url,
             "image_hash": image_hash,
             "call_to_action": call_to_action or {"type": "LEARN_MORE", "value": {"link": link_url}}
         }
    
    payload = {
        "name": name,
        "object_story_spec": spec
    }
    return await client.post(f"/{ad_account_id}/adcreatives", data=payload)

async def upload_image_from_file(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    file_path: Annotated[str, Field(description="Local file path to image.")]
) -> dict:
    """Uploads an image from a local file to the ad account's image library."""
    client = await MetaAPIClient.initialize()
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image not found at {file_path}")
        
    with open(file_path, "rb") as f:
        files = {"filename": f}
        return await client.post(f"/{ad_account_id}/adimages", files=files)

async def upload_image_from_url(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    url: Annotated[str, Field(description="Public URL of the image.")]
) -> dict:
    """Uploads an image from a URL to the ad account's image library."""
    client = await MetaAPIClient.initialize()
    
    # Download the image to a temp file first since Meta API requires multipart for adimages
    # or you can pass 'bytes' directly. Using httpx to fetch.
    async with httpx.AsyncClient() as http:
         resp = await http.get(url)
         resp.raise_for_status()
         file_bytes = resp.content
         
    files = {"filename": ("image.jpg", file_bytes, "image/jpeg")}
    return await client.post(f"/{ad_account_id}/adimages", files=files)

async def upload_video_from_file(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    file_path: Annotated[str, Field(description="Local file path.")], 
    title: Annotated[str, Field(description="Video title.")], 
    description: Annotated[str, Field(description="Video description.")]
) -> dict:
    """Uploads a video to the ad account."""
    client = await MetaAPIClient.initialize()
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video not found at {file_path}")
        
    with open(file_path, "rb") as f:
        files = {"source": f}
        data = {"title": title, "description": description}
        return await client.post(f"/{ad_account_id}/advideos", data=data, files=files)

async def get_video_upload_status(video_id: Annotated[str, Field(description="Video ID.")]) -> dict:
    """Checks the processing status of a video."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{video_id}", params={"fields": "status"})

async def get_creative(
    creative_id: Annotated[str, Field(description="Creative ID.")], 
    fields: Annotated[List[str], Field(description="Fields to return.")] = ["id", "name", "body", "title", "object_story_spec"]
) -> dict:
    """Gets a creative by ID."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{creative_id}", params={"fields": fields})

async def list_creatives(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    limit: Annotated[int, Field(description="Max limits.")] = 25, 
    after: Annotated[Optional[str], Field(description="Pagination cursor.")] = None
) -> dict:
    """Lists creatives in an account."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "id,name", "limit": limit}
    if after: params["after"] = after
    return await client.get(f"/{ad_account_id}/adcreatives", params=params)

async def delete_creative(creative_id: Annotated[str, Field(description="Creative ID.")]) -> dict:
    """Deletes a creative."""
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{creative_id}")

async def get_creative_previews(
    creative_id: Annotated[str, Field(description="Creative ID.")], 
    ad_format: Annotated[str, Field(description="Format placement (e.g. DESKTOP_FEED_STANDARD).")]
) -> dict:
    """Gets preview HTML for a creative."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{creative_id}/previews", params={"ad_format": ad_format})

async def create_instant_experience(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    page_id: Annotated[str, Field(description="Facebook Page ID.")], 
    body_elements: Annotated[List[Dict[str, Any]], Field(description="List of Canvas elements.")], 
    background_color: Annotated[str, Field(description="Hex color code.")], 
    enable_swipe_to_open: Annotated[bool, Field(description="Enable swipe to open.")]
) -> dict:
    """Creates a Canvas (Instant Experience)."""
    client = await MetaAPIClient.initialize()
    payload = {
        "page_id": page_id,
        "canvas_body_elements": body_elements,
        "background_color": background_color,
        "enable_swipe_to_open": enable_swipe_to_open
    }
    return await client.post(f"/{ad_account_id}/canvases", data=payload)

async def get_instant_experience(canvas_id: Annotated[str, Field(description="Canvas ID.")]) -> dict:
    """Gets an Instant Experience."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{canvas_id}", params={"fields": "id,name,elements,background_color"})

async def list_instant_experiences(page_id: Annotated[str, Field(description="Facebook Page ID.")], limit: Annotated[int, Field(description="Result limit.")] = 25) -> dict:
    """Lists Instant Experiences owned by a page."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{page_id}/canvases", params={"limit": limit, "fields": "id,name"})
