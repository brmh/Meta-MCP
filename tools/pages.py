from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

async def get_page(page_id: Annotated[str, Field(description="Facebook Page ID.")]) -> dict:
    """Gets basic info about a Facebook Page."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{page_id}", params={"fields": "id,name,access_token,link"})

async def list_pages() -> dict:
    """Lists pages managed by the user token."""
    client = await MetaAPIClient.initialize()
    return await client.get("/me/accounts", params={"fields": "id,name,access_token,category"})
