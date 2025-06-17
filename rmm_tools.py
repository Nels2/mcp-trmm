from typing import Any
import httpx, sqlite3, json
from mcp.server.fastmcp import FastMCP
from config import *

# Initialize MCP
mcp = FastMCP("trmm-api-agent")

EXTERNAL_API_BASE = "https://api.trmm.org"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

async def make_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None) -> dict[str, Any] | None:
    headers = headers or {}
    headers["User-Agent"] = USER_AGENT
    async with httpx.AsyncClient() as client:
        try:
            func = getattr(client, method.lower())
            response = await func(url, headers=headers, json=data, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def search_endpoint(query: str):
    conn = sqlite3.connect("api_schema4_rmm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path, method, description, request_body, responses FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return [{"path": p, "method": m, "description": d,
             "request_body": json.loads(rb) if rb != "None" else None,
             "responses": json.loads(r)} for p, m, d, rb, r in results]

@mcp.tool()
async def query_api(query: str) -> str:
    results = search_endpoint(query)
    if not results:
        return json.dumps({"error": "No matching endpoints found"})
    return json.dumps({"available_paths": [
        {"path": e["path"], "description": e["description"], "method": e["method"]} for e in results
    ]})

@mcp.tool()
async def run_api(query: str, method: str, payload: dict = None) -> str:
    headers = {"X-API-KEY": xcred}
    response = await make_request(f"{EXTERNAL_API_BASE}{query}", method, headers=headers, data=payload)
    return response

# Optional if running standalone
if __name__ == "__main__":
    mcp.run(transport='stdio')
