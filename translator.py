from __future__ import annotations

from typing import Any, Literal


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def translate_list_agents() -> dict[str, Any]:
    return {
        "action": "list_agents",
        "path": "/agents/",
        "method": "GET",
    }


def translate_get_agent(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent",
        "path": f"/agents/{agent_id}/",
        "method": "GET",
    }


def translate_list_agent_checks(agent_id: str) -> dict[str, Any]:
    return {
        "action": "list_agent_checks",
        "path": f"/agents/{agent_id}/checks/",
        "method": "GET",
    }


def translate_run_checks(agent_id: str, check_ids: list[int] | None = None) -> dict[str, Any]:
    body = {"check_ids": check_ids} if check_ids else None
    return {
        "action": "run_checks",
        "path": f"/agents/{agent_id}/checks/",
        "method": "POST",
        "json_body": body,
    }


def translate_run_agent_command(
    agent_id: str,
    command: str,
    shell: Literal["cmd", "powershell", "bash"] = "cmd",
) -> dict[str, Any]:
    return {
        "action": "run_agent_command",
        "path": f"/agents/{agent_id}/cmd/",
        "method": "POST",
        "json_body": {
            "command": command,
            "shell": shell,
        },
    }


def translate_run_agent_script(
    agent_id: str,
    script_name: str | None = None,
    script_id: int | None = None,
    args: list[str] | None = None,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    timeout_seconds = clamp(timeout_seconds, 5, 1800)

    body: dict[str, Any] = {"timeout": timeout_seconds}
    if script_id is not None:
        body["script"] = script_id
    elif script_name:
        body["script_name"] = script_name
    else:
        raise ValueError("Either script_id or script_name is required.")

    if args:
        body["args"] = args

    return {
        "action": "run_agent_script",
        "path": f"/agents/{agent_id}/runscript/",
        "method": "POST",
        "json_body": body,
    }


def translate_get_agent_history(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent_history",
        "path": f"/agents/{agent_id}/history/",
        "method": "GET",
    }


def translate_get_agent_notes(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent_notes",
        "path": f"/agents/{agent_id}/notes/",
        "method": "GET",
    }


def translate_create_agent_note(agent_id: str, note: str) -> dict[str, Any]:
    return {
        "action": "create_agent_note",
        "path": f"/agents/{agent_id}/notes/",
        "method": "POST",
        "json_body": {
            "note": note,
        },
    }


def translate_get_agent_tasks(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent_tasks",
        "path": f"/agents/{agent_id}/tasks/",
        "method": "GET",
    }


def translate_create_agent_task(agent_id: str, title: str, details: str = "") -> dict[str, Any]:
    return {
        "action": "create_agent_task",
        "path": f"/agents/{agent_id}/tasks/",
        "method": "POST",
        "json_body": {
            "title": title,
            "details": details,
        },
    }


def translate_get_agent_eventlog(
    agent_id: str,
    log_type: str,
    days: int = 1,
) -> dict[str, Any]:
    days = clamp(days, 1, 30)
    return {
        "action": "get_agent_eventlog",
        "path": f"/agents/{agent_id}/eventlog/{log_type}/{days}/",
        "method": "GET",
    }


def translate_list_agent_processes(agent_id: str) -> dict[str, Any]:
    return {
        "action": "list_agent_processes",
        "path": f"/agents/{agent_id}/processes/",
        "method": "GET",
    }


def translate_get_agent_process(agent_id: str, pid: int) -> dict[str, Any]:
    return {
        "action": "get_agent_process",
        "path": f"/agents/{agent_id}/processes/{pid}/",
        "method": "GET",
    }


def translate_kill_agent_process(agent_id: str, pid: int) -> dict[str, Any]:
    return {
        "action": "kill_agent_process",
        "path": f"/agents/{agent_id}/processes/{pid}/",
        "method": "DELETE",
    }


def translate_reboot_agent(
    agent_id: str,
    mode: Literal["normal", "force"] = "normal",
) -> dict[str, Any]:
    if mode == "normal":
        return {
            "action": "reboot_agent",
            "path": f"/agents/{agent_id}/reboot/",
            "method": "POST",
        }

    return {
        "action": "reboot_agent",
        "path": f"/agents/{agent_id}/reboot/",
        "method": "PATCH",
        "json_body": {"force": True},
    }


def translate_shutdown_agent(agent_id: str) -> dict[str, Any]:
    return {
        "action": "shutdown_agent",
        "path": f"/agents/{agent_id}/shutdown/",
        "method": "POST",
    }


def translate_wake_agent(agent_id: str) -> dict[str, Any]:
    return {
        "action": "wake_agent",
        "path": f"/agents/{agent_id}/wol/",
        "method": "POST",
    }
    
def translate_list_report_history() -> dict[str, Any]:
    return {
        "action": "list_report_history",
        "path": "/reporting/history/",
        "method": "GET",
    }


def translate_run_report_history(history_id: int) -> dict[str, Any]:
    return {
        "action": "run_report_history",
        "path": f"/reporting/history/{history_id}/run/",
        "method": "POST",
    }


def translate_list_report_schedules() -> dict[str, Any]:
    return {
        "action": "list_report_schedules",
        "path": "/reporting/schedules/",
        "method": "GET",
    }


def translate_get_report_schedule(schedule_id: int) -> dict[str, Any]:
    return {
        "action": "get_report_schedule",
        "path": f"/reporting/schedules/{schedule_id}/",
        "method": "GET",
    }


def translate_run_report_schedule(schedule_id: int) -> dict[str, Any]:
    return {
        "action": "run_report_schedule",
        "path": f"/reporting/schedules/{schedule_id}/run/",
        "method": "POST",
    }


def translate_list_report_templates() -> dict[str, Any]:
    return {
        "action": "list_report_templates",
        "path": "/reporting/templates/",
        "method": "GET",
    }


def translate_get_report_template(template_id: int) -> dict[str, Any]:
    return {
        "action": "get_report_template",
        "path": f"/reporting/templates/{template_id}/",
        "method": "GET",
    }


def translate_run_report_template(template_id: int) -> dict[str, Any]:
    return {
        "action": "run_report_template",
        "path": f"/reporting/templates/{template_id}/run/",
        "method": "POST",
    }
    
def translate_get_agent_software(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent_software",
        "path": f"/software/{agent_id}/",
        "method": "GET",
    }


def translate_uninstall_agent_software(agent_id: str, software_name: str) -> dict[str, Any]:
    return {
        "action": "uninstall_agent_software",
        "path": f"/software/{agent_id}/uninstall/",
        "method": "POST",
        "json_body": {
            "software": software_name,
        },
    }


def translate_list_choco_packages() -> dict[str, Any]:
    return {
        "action": "list_choco_packages",
        "path": "/software/chocos/",
        "method": "GET",
    }
    
def translate_get_agent_winupdates(agent_id: str) -> dict[str, Any]:
    return {
        "action": "get_agent_winupdates",
        "path": f"/winupdate/{agent_id}/",
        "method": "GET",
    }


def translate_scan_agent_winupdates(agent_id: str) -> dict[str, Any]:
    return {
        "action": "scan_agent_winupdates",
        "path": f"/winupdate/{agent_id}/scan/",
        "method": "POST",
    }


def translate_install_agent_winupdates(agent_id: str) -> dict[str, Any]:
    return {
        "action": "install_agent_winupdates",
        "path": f"/winupdate/{agent_id}/install/",
        "method": "POST",
    }
    
def translate_list_agent_services(agent_id: str) -> dict[str, Any]:
    return {
        "action": "list_agent_services",
        "path": f"/services/{agent_id}/",
        "method": "GET",
    }


def translate_get_agent_service(agent_id: str, service_name: str) -> dict[str, Any]:
    return {
        "action": "get_agent_service",
        "path": f"/services/{agent_id}/{service_name}/",
        "method": "GET",
    }


def translate_control_agent_service(
    agent_id: str,
    service_name: str,
    action: Literal["start", "stop", "restart"],
) -> dict[str, Any]:
    return {
        "action": "control_agent_service",
        "path": f"/services/{agent_id}/{service_name}/",
        "method": "POST",
        "json_body": {
            "action": action,
        },
    }
    
def translate_list_scripts() -> dict[str, Any]:
    return {
        "action": "list_scripts",
        "path": "/scripts/",
        "method": "GET",
    }


def translate_get_script(script_id: int) -> dict[str, Any]:
    return {
        "action": "get_script",
        "path": f"/scripts/{script_id}/",
        "method": "GET",
    }


def translate_download_script(script_id: int) -> dict[str, Any]:
    return {
        "action": "download_script",
        "path": f"/scripts/{script_id}/download/",
        "method": "GET",
    }


def translate_test_script_on_agent(
    agent_id: str,
    script_id: int | None = None,
    script_name: str | None = None,
    args: list[str] | None = None,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    timeout_seconds = clamp(timeout_seconds, 5, 1800)

    body: dict[str, Any] = {
        "timeout": timeout_seconds,
    }

    if script_id is not None:
        body["script"] = script_id
    elif script_name:
        body["script_name"] = script_name
    else:
        raise ValueError("Either script_id or script_name is required.")

    if args:
        body["args"] = args

    return {
        "action": "test_script_on_agent",
        "path": f"/scripts/{agent_id}/test/",
        "method": "POST",
        "json_body": body,
    }
    
def translate_get_alert(alert_id: int) -> dict[str, Any]:
    return {
        "action": "get_alert",
        "path": f"/alerts/{alert_id}/",
        "method": "GET",
    }


def translate_update_alert_status(
    alert_id: int,
    status: Literal["acknowledged", "resolved", "open"],
) -> dict[str, Any]:
    return {
        "action": "update_alert_status",
        "path": "/alerts/",
        "method": "PATCH",
        "json_body": {
            "id": alert_id,
            "status": status,
        },
    }


def translate_list_alert_templates() -> dict[str, Any]:
    return {
        "action": "list_alert_templates",
        "path": "/alerts/templates/",
        "method": "GET",
    }


def translate_get_alert_template(template_id: int) -> dict[str, Any]:
    return {
        "action": "get_alert_template",
        "path": f"/alerts/templates/{template_id}/",
        "method": "GET",
    }
    
def translate_get_automation_policies_overview() -> dict[str, Any]:
    return {
        "action": "get_automation_policies_overview",
        "path": "/automation/policies/overview/",
        "method": "GET",
    }


def translate_get_automation_policy(policy_id: int) -> dict[str, Any]:
    return {
        "action": "get_automation_policy",
        "path": f"/automation/policies/{policy_id}/",
        "method": "GET",
    }


def translate_list_automation_policy_checks(policy_id: int) -> dict[str, Any]:
    return {
        "action": "list_automation_policy_checks",
        "path": f"/automation/policies/{policy_id}/checks/",
        "method": "GET",
    }


def translate_list_automation_policy_tasks(policy_id: int) -> dict[str, Any]:
    return {
        "action": "list_automation_policy_tasks",
        "path": f"/automation/policies/{policy_id}/tasks/",
        "method": "GET",
    }


def translate_run_automation_task(task_id: int) -> dict[str, Any]:
    return {
        "action": "run_automation_task",
        "path": f"/automation/tasks/{task_id}/run/",
        "method": "POST",
    }


def translate_get_automation_task_status(task_id: int) -> dict[str, Any]:
    return {
        "action": "get_automation_task_status",
        "path": f"/automation/tasks/{task_id}/status/",
        "method": "GET",
    }


def translate_get_automation_check_status(check_id: int) -> dict[str, Any]:
    return {
        "action": "get_automation_check_status",
        "path": f"/automation/checks/{check_id}/status/",
        "method": "GET",
    }
    
def translate_list_checks() -> dict[str, Any]:
    return {
        "action": "list_checks",
        "path": "/checks/",
        "method": "GET",
    }


def translate_get_check(check_id: int) -> dict[str, Any]:
    return {
        "action": "get_check",
        "path": f"/checks/{check_id}/",
        "method": "GET",
    }


def translate_run_checks_for_agent(agent_id: str) -> dict[str, Any]:
    return {
        "action": "run_checks_for_agent",
        "path": f"/checks/{agent_id}/run/",
        "method": "POST",
    }


def translate_reset_check(check_id: int) -> dict[str, Any]:
    return {
        "action": "reset_check",
        "path": f"/checks/{check_id}/reset/",
        "method": "POST",
    }


def translate_reset_all_checks_for_agent(agent_id: str) -> dict[str, Any]:
    return {
        "action": "reset_all_checks_for_agent",
        "path": f"/checks/{agent_id}/resetall/",
        "method": "POST",
    }
    
def translate_list_tasks() -> dict[str, Any]:
    return {
        "action": "list_tasks",
        "path": "/tasks/",
        "method": "GET",
    }


def translate_get_task(task_id: int) -> dict[str, Any]:
    return {
        "action": "get_task",
        "path": f"/tasks/{task_id}/",
        "method": "GET",
    }


def translate_run_task(task_id: int) -> dict[str, Any]:
    return {
        "action": "run_task",
        "path": f"/tasks/{task_id}/run/",
        "method": "POST",
    }
