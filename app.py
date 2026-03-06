from server import mcp

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    # Run the native FastMCP SSE server
    mcp.run(transport="sse", port=port, host="0.0.0.0")
