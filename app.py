import uvicorn
from server import mcp

app = mcp.get_asgi_app()

@app.get("/health")
async def health():
    return {"status": "ok", "server": "meta-ads-mcp", "version": "1.0.0"}

@app.get("/tools")
async def list_tools():
    # Helper to see which tools are registered over HTTP
    return {"tools": [t.name for t in mcp._tool_manager.list_tools()]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info", access_log=True)
