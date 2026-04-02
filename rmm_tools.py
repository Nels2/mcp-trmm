from __future__ import annotations

from typing import Literal
from fastmcp import FastMCP

from api_client import ToolResult, api_request
from translator import (
    translate_list_agents,
    translate_get_agent,
    translate_list_agent_checks,
    translate_run_checks,
    translate_run_agent_command,
    translate_run_agent_script,
    translate_get_agent_history,
    translate_get_agent_notes,
    translate_create_agent_note,
    translate_get_agent_tasks,
    translate_create_agent_task,
    translate_get_agent_eventlog,
    translate_list_agent_processes,
    translate_get_agent_process,
    translate_kill_agent_process,
    translate_reboot_agent,
    translate_shutdown_agent,
    translate_wake_agent,
    translate_list_report_history,
    translate_run_report_history,
    translate_list_report_schedules,
    translate_get_report_schedule,
    translate_run_report_schedule,
    #translate_list_report_templates,
    #translate_get_report_template,
    #translate_run_report_template,
    translate_get_agent_software,
    translate_uninstall_agent_software,
    translate_list_choco_packages,
    translate_get_agent_winupdates,
    translate_scan_agent_winupdates,
    translate_install_agent_winupdates,
    translate_list_agent_services,
    translate_get_agent_service,
    translate_control_agent_service,
    translate_list_scripts,
    translate_get_script,
    translate_download_script,
    translate_test_script_on_agent,
    translate_get_alert,
    translate_update_alert_status,
    #translate_list_alert_templates,
    #translate_get_alert_template,
    translate_get_automation_policies_overview,
    translate_get_automation_policy,
    translate_list_automation_policy_checks,
    translate_list_automation_policy_tasks,
    translate_run_automation_task,
    translate_get_automation_task_status,
    translate_get_automation_check_status,
    translate_list_checks,
    translate_get_check,
    translate_run_checks_for_agent,
    translate_reset_check,
    translate_reset_all_checks_for_agent,
    translate_list_tasks,
    translate_get_task,
    translate_run_task,
)

mcp = FastMCP("trmm-api-agent")


async def _execute(spec: dict) -> ToolResult:
    return await api_request(
        action=spec["action"],
        path=spec["path"],
        method=spec["method"],
        params=spec.get("params"),
        json_body=spec.get("json_body"),
    )


#@mcp.tool()
#async def list_agents() -> ToolResult:
    #"""List all agents."""
    #return await _execute(translate_list_agents())
@mcp.tool()
async def list_agents() -> dict:
    """List all agents."""
    result = await _execute(translate_list_agents())
    if not result.ok:
        return {
            "ok": False,
            "error": result.error,
            "details": result.details,
            "status_code": result.status_code,
        }
    return {
        "ok": True,
        "agents": result.data,
    }


@mcp.tool()
async def get_agent(agent_id: str) -> ToolResult:
    """Get one agent by ID."""
    return await _execute(translate_get_agent(agent_id))


@mcp.tool()
async def get_agent_history(agent_id: str) -> ToolResult:
    """Get history for an agent."""
    return await _execute(translate_get_agent_history(agent_id))

@mcp.tool()
async def get_agent_notes(agent_id: str) -> ToolResult:
    """Get notes for an agent."""
    return await _execute(translate_get_agent_notes(agent_id))


@mcp.tool()
async def create_agent_note(agent_id: str, note: str) -> ToolResult:
    """Create a note for an agent."""
    return await _execute(translate_create_agent_note(agent_id, note))


@mcp.tool()
async def get_agent_tasks(agent_id: str) -> ToolResult:
    """Get tasks for an agent."""
    return await _execute(translate_get_agent_tasks(agent_id))


@mcp.tool()
async def create_agent_task(agent_id: str, title: str, details: str = "") -> ToolResult:
    """Create a task for an agent."""
    return await _execute(translate_create_agent_task(agent_id, title, details))

@mcp.tool()
async def reboot_agent(
    agent_id: str,
    mode: Literal["normal", "force"] = "normal",
) -> ToolResult:
    """Reboot an agent."""
    return await _execute(translate_reboot_agent(agent_id, mode))


@mcp.tool()
async def shutdown_agent(agent_id: str) -> ToolResult:
    """Shut down an agent."""
    return await _execute(translate_shutdown_agent(agent_id))


@mcp.tool()
async def wake_agent(agent_id: str) -> ToolResult:
    """Wake an agent via Wake-on-LAN."""
    return await _execute(translate_wake_agent(agent_id))


@mcp.tool()
async def list_checks() -> ToolResult:
    """List all checks."""
    return await _execute(translate_list_checks())


@mcp.tool()
async def get_check(check_id: int) -> ToolResult:
    """Get one check by ID."""
    return await _execute(translate_get_check(check_id))

@mcp.tool()
async def list_agent_checks(agent_id: str) -> ToolResult:
    """List checks configured on an agent."""
    return await _execute(translate_list_agent_checks(agent_id))


@mcp.tool()
async def run_checks(agent_id: str, check_ids: list[int] | None = None) -> ToolResult:
    """Run all checks, or selected check IDs, for an agent."""
    return await _execute(translate_run_checks(agent_id, check_ids))


@mcp.tool()
async def run_checks_for_agent(agent_id: str) -> ToolResult:
    """Run checks for an agent."""
    return await _execute(translate_run_checks_for_agent(agent_id))


@mcp.tool()
async def reset_check(check_id: int) -> ToolResult:
    """Reset one check by ID."""
    return await _execute(translate_reset_check(check_id))


@mcp.tool()
async def reset_all_checks_for_agent(agent_id: str) -> ToolResult:
    """Reset all checks for an agent."""
    return await _execute(translate_reset_all_checks_for_agent(agent_id))

@mcp.tool()
async def get_agent_software(agent_id: str) -> ToolResult:
    """Get installed software for an agent."""
    return await _execute(translate_get_agent_software(agent_id))


@mcp.tool()
async def uninstall_agent_software(agent_id: str, software_name: str) -> ToolResult:
    """Uninstall a software package from an agent."""
    return await _execute(translate_uninstall_agent_software(agent_id, software_name))


@mcp.tool()
async def list_choco_packages() -> ToolResult:
    """List available Chocolatey package data."""
    return await _execute(translate_list_choco_packages())

@mcp.tool()
async def get_agent_winupdates(agent_id: str) -> ToolResult:
    """Get Windows update status/details for an agent."""
    return await _execute(translate_get_agent_winupdates(agent_id))


@mcp.tool()
async def scan_agent_winupdates(agent_id: str) -> ToolResult:
    """Trigger a Windows update scan on an agent."""
    return await _execute(translate_scan_agent_winupdates(agent_id))


@mcp.tool()
async def install_agent_winupdates(agent_id: str) -> ToolResult:
    """Install pending Windows updates on an agent."""
    return await _execute(translate_install_agent_winupdates(agent_id))


@mcp.tool()
async def list_scripts() -> ToolResult:
    """List available scripts."""
    return await _execute(translate_list_scripts())


@mcp.tool()
async def get_script(script_id: int) -> ToolResult:
    """Get one script by ID."""
    return await _execute(translate_get_script(script_id))


@mcp.tool()
async def download_script(script_id: int) -> ToolResult:
    """Download one script by ID."""
    return await _execute(translate_download_script(script_id))


@mcp.tool()
async def test_script_on_agent(
    agent_id: str,
    script_id: int | None = None,
    script_name: str | None = None,
    args: list[str] | None = None,
    timeout_seconds: int = 90,
) -> ToolResult:
    """Test a script on an agent using script ID or script name."""
    return await _execute(
        translate_test_script_on_agent(
            agent_id=agent_id,
            script_id=script_id,
            script_name=script_name,
            args=args,
            timeout_seconds=timeout_seconds,
        )
    )

@mcp.tool()
async def list_agent_services(agent_id: str) -> ToolResult:
    """List services on an agent."""
    return await _execute(translate_list_agent_services(agent_id))


@mcp.tool()
async def get_agent_service(agent_id: str, service_name: str) -> ToolResult:
    """Get details for one service on an agent."""
    return await _execute(translate_get_agent_service(agent_id, service_name))


@mcp.tool()
async def control_agent_service(
    agent_id: str,
    service_name: str,
    action: Literal["start", "stop", "restart"],
) -> ToolResult:
    """Start, stop, or restart a service on an agent."""
    return await _execute(translate_control_agent_service(agent_id, service_name, action))

@mcp.tool()
async def list_agent_processes(agent_id: str) -> ToolResult:
    """List processes for an agent."""
    return await _execute(translate_list_agent_processes(agent_id))


@mcp.tool()
async def get_agent_process(agent_id: str, pid: int) -> ToolResult:
    """Get a specific process for an agent."""
    return await _execute(translate_get_agent_process(agent_id, pid))


@mcp.tool()
async def kill_agent_process(agent_id: str, pid: int) -> ToolResult:
    """Kill a specific process on an agent."""
    return await _execute(translate_kill_agent_process(agent_id, pid))

@mcp.tool()
async def get_agent_eventlog(agent_id: str, log_type: str, days: int = 1) -> ToolResult:
    """Get event logs for an agent."""
    return await _execute(translate_get_agent_eventlog(agent_id, log_type, days))

@mcp.tool()
async def list_tasks() -> ToolResult:
    """List all tasks."""
    return await _execute(translate_list_tasks())


@mcp.tool()
async def get_task(task_id: int) -> ToolResult:
    """Get one task by ID."""
    return await _execute(translate_get_task(task_id))


@mcp.tool()
async def run_task(task_id: int) -> ToolResult:
    """Run one task immediately."""
    return await _execute(translate_run_task(task_id))







@mcp.tool()
async def run_agent_command(
    agent_id: str,
    command: str,
    shell: Literal["cmd", "powershell", "bash"] = "cmd",
) -> ToolResult:
    """Run a shell command on an agent."""
    return await _execute(translate_run_agent_command(agent_id, command, shell))


@mcp.tool()
async def run_agent_script(
    agent_id: str,
    script_name: str | None = None,
    script_id: int | None = None,
    args: list[str] | None = None,
    timeout_seconds: int = 90,
) -> ToolResult:
    """Run a script on an agent by script ID or script name."""
    return await _execute(
        translate_run_agent_script(
            agent_id=agent_id,
            script_name=script_name,
            script_id=script_id,
            args=args,
            timeout_seconds=timeout_seconds,
        )
    )






@mcp.tool()
async def list_report_history() -> ToolResult:
    """List report run history."""
    return await _execute(translate_list_report_history())


@mcp.tool()
async def run_report_history(history_id: int) -> ToolResult:
    """Rerun a report from report history."""
    return await _execute(translate_run_report_history(history_id))


@mcp.tool()
async def list_report_schedules() -> ToolResult:
    """List configured report schedules."""
    return await _execute(translate_list_report_schedules())


@mcp.tool()
async def get_report_schedule(schedule_id: int) -> ToolResult:
    """Get one report schedule by ID."""
    return await _execute(translate_get_report_schedule(schedule_id))


@mcp.tool()
async def run_report_schedule(schedule_id: int) -> ToolResult:
    """Run a report schedule immediately."""
    return await _execute(translate_run_report_schedule(schedule_id))







    
@mcp.tool()
async def get_alert(alert_id: int) -> ToolResult:
    """Get one alert by ID."""
    return await _execute(translate_get_alert(alert_id))


@mcp.tool()
async def update_alert_status(
    alert_id: int,
    status: Literal["acknowledged", "resolved", "open"],
) -> ToolResult:
    """Update the status of an alert."""
    return await _execute(translate_update_alert_status(alert_id, status))


@mcp.tool()
async def get_automation_policies_overview() -> ToolResult:
    """Get an overview of automation policies."""
    return await _execute(translate_get_automation_policies_overview())


@mcp.tool()
async def get_automation_policy(policy_id: int) -> ToolResult:
    """Get one automation policy by ID."""
    return await _execute(translate_get_automation_policy(policy_id))


@mcp.tool()
async def list_automation_policy_checks(policy_id: int) -> ToolResult:
    """List checks attached to an automation policy."""
    return await _execute(translate_list_automation_policy_checks(policy_id))


@mcp.tool()
async def list_automation_policy_tasks(policy_id: int) -> ToolResult:
    """List tasks attached to an automation policy."""
    return await _execute(translate_list_automation_policy_tasks(policy_id))


@mcp.tool()
async def run_automation_task(task_id: int) -> ToolResult:
    """Run an automation task immediately."""
    return await _execute(translate_run_automation_task(task_id))


@mcp.tool()
async def get_automation_task_status(task_id: int) -> ToolResult:
    """Get status for an automation task."""
    return await _execute(translate_get_automation_task_status(task_id))


@mcp.tool()
async def get_automation_check_status(check_id: int) -> ToolResult:
    """Get status for an automation check."""
    return await _execute(translate_get_automation_check_status(check_id))


