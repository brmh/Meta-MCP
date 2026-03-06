import socket
import httpx
import asyncio

async def run_advanced_debug():
    host = "graph.facebook.com"
    results = {}
    
    # 1. Try Google DNS over HTTPS (DoH) to get the IP manually
    try:
        async with httpx.AsyncClient() as client:
            # Query Google DoH
            params = {"name": host, "type": "A"}
            res = await client.get("https://dns.google/resolve", params=params, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
                results["doh_google"] = f"Success: {ips}"
                results["ips"] = ips
            else:
                results["doh_google"] = f"Failed: Status {res.status_code}"
    except Exception as e:
        results["doh_google"] = f"Failed: {str(e)}"

    # 2. Try Cloudflare DoH
    try:
        async with httpx.AsyncClient() as client:
            headers = {"accept": "application/dns-json"}
            params = {"name": host, "type": "A"}
            res = await client.get("https://cloudflare-dns.com/query", params=params, headers=headers, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                ips = [ans["data"] for ans in data.get("Answer", []) if ans["type"] == 1]
                results["doh_cloudflare"] = f"Success: {ips}"
            else:
                results["doh_cloudflare"] = f"Failed: Status {res.status_code}"
    except Exception as e:
        results["doh_cloudflare"] = f"Failed: {str(e)}"
        
    return results

if __name__ == "__main__":
    print(asyncio.run(advanced_debug()))
