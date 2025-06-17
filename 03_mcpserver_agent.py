from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Optional, Dict, Any
from config import MCP_BEARER_TOKEN
from rmm_tools import mcp, query_api, run_api

# === Bearer Security Definition
security = HTTPBearer(auto_error=False)

def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if not credentials or credentials.credentials != MCP_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials



# === FastAPI App with Global Security Dependency
app = FastAPI(
    title="TRMM API Agent",
    version="1.0.4",
    description="Secure MCP server for TRMM API usage",
    dependencies=[Depends(verify_bearer_token)]
)


# === Request Models
class QueryBody(BaseModel):
    query: str

class RunBody(BaseModel):
    query: str
    method: str
    payload: Optional[Dict[str, Any]] = None



# === MCP Routes
@app.post("/query_api", tags=["RMM Tools"])
async def query_api_route(body: QueryBody, token: str = Security(verify_bearer_token)):
    return await query_api(query=body.query)

@app.post("/run_api", tags=["RMM Tools"])
async def run_api_route(body: RunBody, token: str = Security(verify_bearer_token)):
    return await run_api(query=body.query, method=body.method, payload=body.payload)

# === OpenAPI Swagger Auth Setup # not needed unless you do more than needed, if you get the drift!
#def custom_openapi():
#    if app.openapi_schema:
#        return app.openapi_schema

#    schema = get_openapi(
#        title=app.title,
#        version=app.version,
#        description=app.description,
#        routes=app.routes,
#    )

#    schema["components"]["securitySchemes"] = {
#        "bearerAuth": {
#            "type": "http",
#            "scheme": "bearer"
#        }
#    }
#    schema["security"] = [{"bearerAuth": []}]  # ✅ SWAGGER USES THIS
#    app.openapi_schema = schema
#    return schema

#app.openapi = custom_openapi
