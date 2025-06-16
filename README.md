#  TRMM API Agent (mcp-trmm)
This project is a secure, bearer-authenticated FastAPI wrapper for the Tactical RMM API using the [MCP](https://github.com/jmorganca/mcpo) server and SQLite-backed schema search. It allows querying documented endpoints locally and forwarding live requests securely to the RMM production API. TRMM [https://docs.tacticalrmm.com/functions/api/]


## Features

- Bearer token authentication (works with Swagger UI `/docs`)
- LLM tool integration via MCP (@mcp.tool)
- RAG-like path discovery via SQLite (`api_schema4_rmm.db`)
- OpenWebUI-compatible Swagger generation
- Full local + live production API querying
- SQLite schema builder, YAML to JSON converter, and CLI assistant tools included


## Project Structure

| File                      | Purpose                                                          |
| ------------------------- | ---------------------------------------------------------------- |
| `rmm_tools.py`            | Registers `@mcp.tool()` functions (`query_api`, `run_api`)       |
| `flaskapi_server.py`      | FastAPI app, bearer auth, routes, and Swagger customization      |
| `config.py`               | Contains your `MCP_BEARER_TOKEN` and RMM `xcred` API key         |
| `api_schema4_rmm.db`      | SQLite3 database holding indexed RMM API schema                  |
| `00_convert_yaml_json.py` | Converts RMM `rmm.yaml` spec to JSON format                      |
| `01_create_database.py`   | Loads JSON schema into `api_schema4_rmm.db` for fast path search |
| `02_query_database.py`    | CLI tool to search API schema locally using keywords             |
| `02_debug_relay2RMM.py`   | Flask server that proxies local schema + forwards live requests  |
| `03_llm_cli_rag.py`       | CLI assistant for interacting with schema using local LLM + RAG  |

---

## Project Overview

The primary goal of this project is to parse the **RMM API schema**, store it in a **SQLite3 database**, and use it to augment queries made to the live RMM API. This is accomplished using several components, which work together to:

1. Parse the RMM API schema and store it in an SQLite3 database.
2. Forward API queries to a live production RMM API server.
3. Provide an LLM-powered CLI interface for querying and retrieving paths from the RMM API.

## Components

### 0. `00_convert_yaml_json.py`
`00_convert_yaml_json.py` is designed to convert a YAML file (`rmm.yaml`) into a JSON format and save it as a new file (`rmm_schema.json`).

### 1. `01_create_database.py`
`01_create_database.py` is designed to create a SQLite database (`api_schema4_rmm.db`) from a **JSON schema** (`rmm_schema.json`) containing the RMM API details. It stores API endpoint information, including path, method, description, request body, and responses, in a structured SQLite database. The script reads the **RMM API schema** from a **JSON file**, parses it, and stores relevant API details in a **SQLite database**. It creates a table for storing API endpoints and inserts the data into the table.

### 2. `02_query_database.py`
`02_query_database.py` allows you to **search for API endpoints** in an SQLite3 database (`api_schema4_rmm.db`) by querying a keyword. It retrieves matching paths, methods, descriptions, request body schemas, and response codes from the database and prints the results in a user-friendly format.
  - The script searches the database for endpoints that contain the provided query keyword in the path. e.g; /login
  - It prints the endpoint `path`, HTTP `method`, `description`, `request body schema`, and `response codes`.
  - If the `request body` and `responses` exist, it pretty-prints them as formatted JSON.
  - The data is stored in the `api_schema4_rmm.db` SQLite3 database, which contains the parsed RMM API schema.

    #### 2a. `02_debug_relay2RMM.py`
    This script acts as a **proxy server** for querying an **RMM API schema** stored in a SQLite3 database and forwarding API requests to the live production **RMM API server**. Do not confuse this with an MCP server because this is not it. The script allows you to query the API schema stored in the local SQLite3 database (`api_schema4_rmm.db`) and forward requests to the live **RMM API server**. It acts as a **debug relay**, providing a means to query the API schema and perform requests on the live API based on the schema.
      - The script allows querying the local SQLite3 database for API endpoints based on a search keyword.
      - Once an API endpoint is found, the script forwards the request (GET, POST, PUT, DELETE) to the live **RMM API** (`https://api.trmm.org`).
      - **Swagger UI** is integrated for interactive documentation, allowing users to see available API endpoints and query them with ease.
      - The script gracefully handles unsupported HTTP methods and responds with an error if no matching endpoints are found.




### 3. `03_mcpserver_agent*.py`
`03_mcpserver_agent+auth.py` & `03_mcpserver_agent_noauth.py` act as an **MCP proxy server**, forwarding queries to the live production **RMM API server** (a REST API). It works as a mediator between the local system (where the database is stored) and the live RMM API. The only difference is one uses Bearer Auth, and the other uses no auth.

- **MCP Proxy Server**: Handles requests by querying the local SQLite3 database, fetching matching endpoints, and forwarding the requests to the live RMM API server.
- **Retrieval-Augmented Generation (RAG)**: Retrieves relevant API endpoints from the SQLite3 database and dynamically forwards requests to the live RMM API.
- **Asynchronous Requests**: Uses `httpx` for asynchronous HTTP requests to forward queries to the production API.
  
    #### 3a. `03_flaskapi.py`
    `03_flaskapi.py` serves as the **API endpoint** for querying the SQLite3 database and returning relevant API endpoint paths.

    - **Search and Query**: This script allows you to query the SQLite3 database for specific API paths, methods, and descriptions.
    - **Forward Requests**: After retrieving matching paths, the script forwards the requests to the live RMM API using the **MCP proxy server** (`03_mcpserver.py`).

    #### 3b. `03_llm_cli__rag.py`
    `03_llm_cli__rag.py` is the **command-line interface (CLI)** where users can interact with the **Retrieval-Augmented Generation (RAG)** system using a **Large Language Model (LLM)**.

    - **LLM Querying**: This script allows users to ask questions related to the RMM API paths available in the schema, which is stored in the SQLite3 database.
    - **Simultaneous Execution**: It’s meant to run alongside `03_flaskapi.py`, allowing real-time interaction between the user and the LLM, enabling intelligent querying of the RMM API paths.

## Setup & Installation

### 1. Install dependencies
You will need to install the required dependencies for the project:
**uv / uvx installed from source[https://docs.astral.sh/uv/getting-started/installation/]**
```bash
uv pip install fastapi uvicorn httpx mcpo sqlite3 pyyaml flask requests flasgger 
```

### 2. Build SQLite3 Schema DB (optional)

```bash
python 00_convert_yaml_json.py  # convert to JSON
python 01_create_database.py    # build SQLite DB from schema
```


### 3. **Run the Servers**
You have a few options for running this, read below!

Start the **Local** Flask API Server (03_flaskapi.py):
This server listens for queries about the RMM API schema and forwards requests to the live RMM API server.

```bash
source .venv/bin/activate
python 03_flaskapi.py
```

Start the **Local** LLM CLI Session (03_llm_cli__rag.py):
This script provides a CLI interface where you can query the API paths available in the schema.

```bash
source .venv/bin/activate
python 03_llm_cli__rag.py

```



Run the MCP Proxy Server (03_mcpserver.py), for Open-WebUI or Claude Desktop:
This server forwards requests from the Flask API to the live production RMM API.
```bash
source .venv/bin/activate
uvx mcpo --port 5086 -- uv run 03_mcpserver.py
```


Run the FastAPI Server (secured)
```bash
uvicorn flaskapi_server:app --host 0.0.0.0 --port 5074
```

Then visit: [http://localhost:5074/docs](http://localhost:5074/docs)

### 4. Test with curl

```bash
curl -X POST http://localhost:5074/query_api \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "/User"}'
```

---

## Endpoints

### `POST /query_api`

- Search `api_schema4_rmm.db` for matching paths/methods/descriptions.
- Returns matching endpoints based on partial path or keyword.

### `POST /run_api`

- Forwards request to production RMM API at `https://api.remotelyfx.spaceagefcu.org`.
- Adds `X-API-KEY` header from config.
- Currently supports: GET, POST, PUT, DELETE.

---

## Swagger Auth Setup

- Uses **HTTPBearer** security scheme
- All endpoints are secured with a `Bearer` token
- Click **Authorize** on `/docs` page and paste your token once

---

## Dev Notes

- Based on previous MCP projects like `scale-api-agent` and `365-sacu-email-server`
- SQLite3 path database created via earlier `01_create_database.py` tooling
- LLM tooling (RAG + CLI) lives in separate modules (`03_llm_cli_rag.py` etc.)

## Optional Tooling for Dev/Debug

### 02\_debug\_relay2RMM.py

A Swagger-enabled relay that lets you test requests from the local SQLite schema DB and forward them to the live RMM API for live previewing and prototyping.

### 03\_llm\_cli\_rag.py

LLM-powered CLI agent for asking natural language questions about the schema.

```bash
python 03_llm_cli_rag.py
💡 Ask a question about the API: /users
```


## Use Cases

- Secure programmatic access to RMM endpoints from LLM tools
- Offline schema exploration using SQLite and local tools
- Developer-friendly curl/CLI testing via `run_api`
- OpenWebUI integration for autonomous agents


---

## License

MIT — use this with your RMM infrastructure or automate your own endpoints.


