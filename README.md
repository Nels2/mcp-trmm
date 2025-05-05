# mcp-trmm
This project is designed to interact with the **Tactical Remote Monitoring and Management (TRMM) API**, create an **SQLite3 database** from the API schema, and enable **Retrieval-Augmented Generation (RAG)** to enhance interaction with the API. It includes a set of tools to query the RMM API schema, forward requests to the live production RMM API server, and provide an LLM-powered CLI interface for exploring available paths.

https://docs.tacticalrmm.com/functions/api/

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




### 3. `03_mcpserver.py`
`03_mcpserver.py` acts as an **MCP proxy server**, forwarding queries to the live production **RMM API server** (a REST API). It works as a mediator between the local system (where the database is stored) and the live RMM API.

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

### Workflow

1. **Run `03_flaskapi.py`**: This script exposes an API that allows you to query the local SQLite3 database for API paths, methods, and descriptions.

   - Use the `POST /query` endpoint to search for API endpoints in the local schema.
   - Example request:
     ```bash
     curl -X 'POST' \
       'http://127.0.0.1:5086/query' \
       -H 'Content-Type: application/json' \
       -d '{"query": "/agents", "api_key": "your_api_key"}'
     ```

2. **Run `03_llm_cli__rag.py`**: This script allows you to query the available paths using the LLM, which leverages the SQLite3 database to find relevant API paths dynamically.

   - It works by asking the LLM about the available API paths and their details.
   - Example CLI usage:
     ```bash
     python 03_llm_cli__rag.py
     ```

3. **Query the Live API**: Once the path is retrieved, `03_mcpserver.py` forwards the request to the live production **RMM API** server. The response from the live API is then returned to the user.

---

## Setup and Installation

### 1. **Install Dependencies**
You will need to install the required dependencies for the project:
**uv / uvx installed from source[https://docs.astral.sh/uv/getting-started/installation/]**
```bash
pip install fastapi uvicorn httpx mcpo sqlite3 pyyaml flask requests flasgger 
```
### 2. **Run the Servers**
Start the **Local** Flask API Server (03_flaskapi.py):
This server listens for queries about the RMM API schema and forwards requests to the live RMM API server.

```bash
source venv/bin/activate
python 03_flaskapi.py
```

Start the **Local** LLM CLI Session (03_llm_cli__rag.py):
This script provides a CLI interface where you can query the API paths available in the schema.

```bash
source venv/bin/activate
python 03_llm_cli__rag.py
```

Run the MCP Proxy Server (03_mcpserver.py), for Open-WebUI or Claude Desktop:
This server forwards requests from the Flask API to the live production RMM API.
```bash
source venv/bin/activate
uvx mcpo --port 5086 -- uv run 03_mcpserver.py
```



### 3. **Interacting with the API:**
You can now send queries using the CLI or directly interact with the Flask API to search for endpoints and forward requests to the live RMM API.


## Use Cases
### 1. Schema Exploration:
You can dynamically query the API schema stored in the SQLite3 database and explore the available paths, methods, and descriptions.

### 2. Forward Requests to Live API:
Once the relevant endpoints are retrieved from the local database, the server forwards the requests to the live RMM API, allowing you to interact with the live production system.

### 3. RAG (Retrieval-Augmented Generation):
The integration of RAG allows for more intelligent and context-aware queries of the RMM API, making it easier to interact with the API based on real-time context and query responses.
