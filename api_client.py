from __future__ import annotations

from typing import Any
import httpx
from pydantic import BaseModel

from config import xcred

EXTERNAL_API_BASE = "https://api.remotelyfx.spaceagefcu.org"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)


class ToolResult(BaseModel):
    ok: bool
    action: str
    status_code: int | None = None
    request_method: str | None = None
    request_path: str | None = None
    data: Any | None = None
    error: str | None = None
    details: str | None = None


async def api_request(
    *,
    action: str,
    path: str,
    method: str,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> ToolResult:
    headers = {
        "X-API-KEY": xcred,
        "User-Agent": USER_AGENT,
    }
    url = f"{EXTERNAL_API_BASE}{path}"

    async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
        try:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=json_body,
            )

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type.lower():
                data = response.json()
            else:
                data = response.text

            response.raise_for_status()

            return ToolResult(
                ok=True,
                action=action,
                status_code=response.status_code,
                request_method=method.upper(),
                request_path=path,
                data=data,
            )

        except httpx.HTTPStatusError as e:
            return ToolResult(
                ok=False,
                action=action,
                status_code=e.response.status_code,
                request_method=method.upper(),
                request_path=path,
                error=str(e),
                details=e.response.text,
            )
        except Exception as e:
            return ToolResult(
                ok=False,
                action=action,
                request_method=method.upper(),
                request_path=path,
                error=str(e),
            )
