from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

async def create_catalog(business_id: Annotated[str, Field(description="Business ID.")], name: Annotated[str, Field(description="Name.")], vertical: Annotated[str, Field(description="E.g., commerce, vehicles.")]) -> dict:
    """Creates a catalog."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{business_id}/product_catalogs", data={"name": name, "vertical": vertical})

async def get_catalog(catalog_id: Annotated[str, Field(description="Catalog ID.")], fields: Annotated[List[str], Field(description="Fields.")] = ["id", "name", "vertical"]) -> dict:
    """Gets catalog details."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{catalog_id}", params={"fields": fields})

async def list_catalogs(business_id: Annotated[str, Field(description="Business ID.")]) -> dict:
    """Lists catalogs for a business."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{business_id}/owned_product_catalogs", params={"fields": "id,name"})

async def delete_catalog(catalog_id: Annotated[str, Field(description="Catalog ID.")]) -> dict:
    """Deletes a catalog."""
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{catalog_id}")

async def create_product_feed(
    catalog_id: Annotated[str, Field(description="Catalog ID.")],
    name: Annotated[str, Field(description="Feed Name.")],
    schedule: Annotated[Dict[str, Any], Field(description="Schedule dictionary.")],
    file_name: Annotated[Optional[str], Field(description="Remote file name/url.")] = None,
    encoding: Annotated[str, Field(description="E.g., utf-8.")] = "utf-8",
    delimiter: Annotated[str, Field(description="E.g., COMMA, TAB.")] = "COMMA"
) -> dict:
    """Creates a product feed for a catalog."""
    client = await MetaAPIClient.initialize()
    payload = {
        "name": name,
        "schedule": schedule,
        "encoding": encoding,
        "delimiter": delimiter
    }
    if file_name: payload["file_name"] = file_name
    return await client.post(f"/{catalog_id}/product_feeds", data=payload)

async def get_product_feed(feed_id: Annotated[str, Field(description="Feed ID.")]) -> dict:
    """Gets feed info."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{feed_id}", params={"fields": "id,name,schedule"})

async def list_product_feeds(catalog_id: Annotated[str, Field(description="Catalog ID.")]) -> dict:
    """Lists feeds for a catalog."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{catalog_id}/product_feeds", params={"fields": "id,name"})

async def delete_product_feed(feed_id: Annotated[str, Field(description="Feed ID.")]) -> dict:
    """Deletes feed."""
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{feed_id}")

async def trigger_product_feed_upload(feed_id: Annotated[str, Field(description="Feed ID.")]) -> dict:
    """Forces an immediate pull of a scheduled product feed."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{feed_id}/uploads")

async def get_feed_upload_history(feed_id: Annotated[str, Field(description="Feed ID.")], limit: Annotated[int, Field(description="Result limit.")] = 10) -> dict:
    """Gets feed upload history."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{feed_id}/uploads", params={"limit": limit})

async def list_products(
    catalog_id: Annotated[str, Field(description="Catalog ID.")], 
    filter: Annotated[Optional[str], Field(description="JSON filter string.")] = None, 
    limit: Annotated[int, Field(description="Result limit.")] = 50
) -> dict:
    """Lists individual products in a catalog."""
    client = await MetaAPIClient.initialize()
    params = {"limit": limit, "fields": "id,name,availability,price,image_url"}
    if filter: params["filter"] = filter
    return await client.get(f"/{catalog_id}/products", params=params)

async def get_product(product_id: Annotated[str, Field(description="Product ID.")], fields: Annotated[List[str], Field(description="Fields to return.")]) -> dict:
    """Gets a specific product item."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{product_id}", params={"fields": fields})

async def create_product_set(
    catalog_id: Annotated[str, Field(description="Catalog ID.")], 
    name: Annotated[str, Field(description="Product Set Name.")], 
    filter: Annotated[Dict[str, Any], Field(description="Filter logic.")]
) -> dict:
    """Creates a subset of products in a catalog."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{catalog_id}/product_sets", data={"name": name, "filter": filter})

async def get_product_set(product_set_id: Annotated[str, Field(description="Product Set ID.")]) -> dict:
    """Gets product set."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{product_set_id}", params={"fields": "id,name,filter"})

async def list_product_sets(catalog_id: Annotated[str, Field(description="Catalog ID.")]) -> dict:
    """Lists sets in a catalog."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{catalog_id}/product_sets", params={"fields": "id,name"})

async def delete_product_set(product_set_id: Annotated[str, Field(description="Product Set ID.")]) -> dict:
    """Deletes product set."""
    client = await MetaAPIClient.initialize()
    return await client.delete(f"/{product_set_id}")
