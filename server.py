from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import MCP_BEARER_TOKEN
from rmm_tools import mcp

mcp_app = mcp.http_app(path="/")

app = FastAPI(
    title="TRMM MCP Server",
    version="2.1.0",
    description="Secure MCP server for TRMM agent tools",
    lifespan=mcp_app.lifespan,
)


@app.middleware("http")
async def verify_bearer_token(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        auth_header = request.headers.get("authorization")
        expected = f"Bearer {MCP_BEARER_TOKEN}"

        if auth_header != expected:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"},
            )

    return await call_next(request)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


app.mount("/mcp", mcp_app)
