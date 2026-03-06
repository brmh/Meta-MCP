from fastmcp import FastMCP
from config.settings import settings
from auth.token_manager import TokenManager
from api.client import MetaAPIClient
import inspect

mcp = FastMCP(
    name="meta-ads-mcp",
    version="1.0.0"
)

import tools.campaigns
import tools.adsets
import tools.ads
import tools.creatives
import tools.audiences
import tools.insights
import tools.pixels
import tools.catalogs
import tools.pages
import tools.billing
import tools.debug
import tools.targeting

# Dynamically register all tools 
modules = [
    tools.campaigns, tools.adsets, tools.ads, tools.creatives,
    tools.audiences, tools.insights, tools.pixels, tools.catalogs,
    tools.pages, tools.billing, tools.debug
]

for mod in modules:
    for name, func in inspect.getmembers(mod, inspect.iscoroutinefunction):
        if not name.startswith("_"):
            mcp.tool()(func)

@mcp.resource("meta://account/{ad_account_id}")
async def get_account_resource(ad_account_id: str) -> str:
    client = await MetaAPIClient.initialize()
    result = await client.get(f"/{ad_account_id}", {"fields": "name,currency,timezone_name,account_status"})
    return str(result)


