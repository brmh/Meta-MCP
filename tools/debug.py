import socket
import httpx
from typing import Annotated, Dict
from pydantic import Field

async def debug_network(host: Annotated[str, Field(description="Host to test DNS for.")] = "graph.facebook.com") -> dict:
    """Diagnostic tool to test network connectivity from the server."""
    results = {}
    
    # 1. DNS check
    try:
        ip = socket.gethostbyname(host)
        results["dns_resolution"] = f"Success: {ip}"
    except Exception as e:
        results["dns_resolution"] = f"Failed: {str(e)}"
        
    # 2. HTTP check
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"https://{host}", timeout=5.0)
            results["http_check"] = f"Status {res.status_code}"
    except Exception as e:
        results["http_check"] = f"Failed: {str(e)}"
        
    return results
