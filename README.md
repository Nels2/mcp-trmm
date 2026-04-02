# TRMM MCP Server

A focused MCP server for TRMM-style remote management operations.

This project exposes a curated set of MCP tools for common IT operations tasks such as:

- agent lookup and control
- checks
- scripts
- services
- software
- Windows updates
- reporting
- alerts
- automation
- tasks

The server is designed specifically for **local or smaller models** that are not reliable at constructing raw API paths, HTTP methods, or JSON payloads.

Instead of exposing one generic “call any endpoint” tool, this server exposes **small, strongly-named tools** with only a few arguments. The backend then translates those arguments into valid API requests.

## Why this exists

Smaller local models tend to struggle with:

- choosing the correct endpoint
- selecting the right HTTP method
- building valid JSON payloads
- keeping IDs and object types straight
- avoiding destructive or overly broad actions

This server solves that by giving the model:

- a small tool surface
- explicit tool names
- simple arguments
- backend-side request translation
- consistent result handling

In short, the model decides **what it wants to do**, and the backend decides **how to call the real API**.

---

## Architecture

The project is split into four main layers:

### `server.py`
Hosts the FastAPI application and mounts the MCP ASGI app at `/mcp`.

Also includes:

- bearer token protection for the MCP route
- a simple `/healthz` endpoint

### `rmm_tools.py`
Defines the MCP tools exposed to the model.

These are the only functions the model should see.

Examples:

- `list_agents()`
- `get_agent(agent_id)`
- `reboot_agent(agent_id, mode="normal")`
- `run_agent_command(agent_id, command, shell="cmd")`

### `translator.py`
Converts model-friendly arguments into actual API requests.

This layer handles:

- endpoint selection
- method selection
- JSON body construction
- argument normalization
- simple action mapping

Example:

- model calls `reboot_agent(agent_id="abc", mode="force")`
- translator turns that into `PATCH /agents/{agent_id}/reboot/` with the correct request body

### `api_client.py`
Sends the final HTTP request to the upstream TRMM/PAI API and returns a normalized result object.

This layer handles:

- authentication headers
- timeouts
- JSON parsing
- status handling
- structured error reporting

---

## Design goals

This MCP server is intentionally opinionated.

### 1. Small tool surface
The server only includes **useful** tools, not every endpoint in the upstream schema.

### 2. Model-friendly tools
Each tool is designed to be easy for a smaller model to call correctly.

### 3. Read-first behavior
Where possible, the model should inspect first and act second.

### 4. Backend-owned request formatting
The model should never be responsible for building raw endpoint paths or request payloads.

### 5. Safer operations
Destructive or state-changing tools are kept limited and clearly named.

---

## Current tool coverage

## Agents
- `list_agents`
- `get_agent`
- `get_agent_history`
- `get_agent_notes`
- `create_agent_note`
- `get_agent_tasks`
- `create_agent_task`
- `reboot_agent`
- `shutdown_agent`
- `wake_agent`
- `run_agent_command`
- `run_agent_script`
- `get_agent_eventlog`
- `list_agent_processes`
- `get_agent_process`
- `kill_agent_process`

## Checks
- `list_checks`
- `get_check`
- `list_agent_checks`
- `run_checks`
- `run_checks_for_agent`
- `reset_check`
- `reset_all_checks_for_agent`

## Software
- `get_agent_software`
- `uninstall_agent_software`
- `list_choco_packages`

## Windows Updates
- `get_agent_winupdates`
- `scan_agent_winupdates`
- `install_agent_winupdates`

## Services
- `list_agent_services`
- `get_agent_service`
- `control_agent_service`

## Scripts
- `list_scripts`
- `get_script`
- `download_script`
- `test_script_on_agent`

## Reporting
- `list_report_history`
- `run_report_history`
- `list_report_schedules`
- `get_report_schedule`
- `run_report_schedule`

## Alerts
- `get_alert`
- `update_alert_status`

## Automation
- `get_automation_policies_overview`
- `get_automation_policy`
- `list_automation_policy_checks`
- `list_automation_policy_tasks`
- `run_automation_task`
- `get_automation_task_status`
- `get_automation_check_status`

## Tasks
- `list_tasks`
- `get_task`
- `run_task`

---

## What is intentionally not included

This server does **not** attempt to expose every endpoint from the upstream schema.

The following kinds of endpoints are intentionally avoided unless they are truly needed:

- generic CRUD for every object type
- broad administrative mutation endpoints
- highly ambiguous update endpoints
- raw pass-through API tools
- configuration-heavy endpoints that require large request bodies
- tools that overlap too heavily with clearer existing tools

This keeps the model from being overwhelmed and reduces incorrect tool selection.

---

## Example tool behavior

### Example 1: Reboot an agent by name
The model should:

1. call `list_agents`
2. identify the correct agent
3. call `reboot_agent(agent_id, mode="normal")`

### Example 2: Investigate a service issue
The model should:

1. find the agent
2. call `get_agent_service(...)` or `list_agent_services(...)`
3. inspect the result
4. only then call `control_agent_service(...)` if requested or clearly appropriate

### Example 3: Check Windows updates
The model should:

1. call `get_agent_winupdates(agent_id)`
2. inspect the result
3. only call `scan_agent_winupdates(...)` or `install_agent_winupdates(...)` when requested

---

## Running the server

Start the FastAPI app with Uvicorn:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
