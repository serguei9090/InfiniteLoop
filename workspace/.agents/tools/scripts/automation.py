"""
Automation Tool - Scripts Category
Handles automation tasks, scheduled jobs, and workflow orchestration.
"""


class AutomationTool:
    """
    Tool for automation operations.

    Capabilities:
    - Schedule tasks
    - Run workflows
    - Monitor processes
    - Handle cron-like scheduling
    """

    name = "automation"
    description = (
        "Schedule tasks, run workflows, monitor processes, and handle automation"
    )
    category = "scripts"

    def __init__(self):
        self.scheduled_tasks = {}
        self.workflow_count = 0

    async def execute(self, args: dict) -> dict:
        """Execute automation operation."""
        action = args.get("action", "")

        if action == "schedule":
            return await self._schedule_task(args)
        elif action == "cancel":
            return await self._cancel_task(args)
        elif action == "list":
            return await self._list_tasks(args)
        elif action == "run_workflow":
            return await self._run_workflow(args)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}

    async def _schedule_task(self, args: dict) -> dict:
        """Schedule a recurring task."""
        name = args.get("name", "")
        command = args.get("command", "")
        interval = args.get("interval", "60")  # seconds

        if not name or not command:
            return {"success": False, "error": "Missing required fields: name, command"}

        # Check for duplicate
        if name in self.scheduled_tasks:
            return {"success": False, "error": f"Task already scheduled: {name}"}

        task = {
            "name": name,
            "command": command,
            "interval": interval,
            "status": "scheduled",
            "created_at": args.get("timestamp", None),
        }

        self.scheduled_tasks[name] = task

        return {
            "success": True,
            "message": f"Scheduled task: {name} every {interval}s",
            "operation": "schedule",
            "task": task,
        }

    async def _cancel_task(self, args: dict) -> dict:
        """Cancel a scheduled task."""
        name = args.get("name", "")

        if name in self.scheduled_tasks:
            cancelled = self.scheduled_tasks.pop(name)

            return {
                "success": True,
                "message": f"Cancelled task: {name}",
                "operation": "cancel",
                "task": cancelled,
            }
        else:
            return {"success": False, "error": f"Task not found: {name}"}

    async def _list_tasks(self, args: dict) -> dict:
        """List scheduled tasks."""
        filter_status = args.get("status", None)

        tasks = list(self.scheduled_tasks.values())

        if filter_status:
            tasks = [t for t in tasks if t["status"] == filter_status]

        return {
            "success": True,
            "operation": "list",
            "count": len(tasks),
            "tasks": tasks,
        }

    async def _run_workflow(self, args: dict) -> dict:
        """Run a workflow."""
        workflow_name = args.get("name", "")
        steps = args.get("steps", [])

        if not workflow_name or not steps:
            return {"success": False, "error": "Missing required fields: name, steps"}

        self.workflow_count += 1

        results = []
        for step in steps:
            step_name = step.get("name", "")
            action = step.get("action", "")

            try:
                result = await self._execute_step(step)
                results.append({"step": step_name, "result": result})
            except Exception as e:
                results.append({"step": step_name, "error": str(e)})

        return {
            "success": True,
            "operation": "run_workflow",
            "workflow": workflow_name,
            "steps_count": len(steps),
            "successful": sum(1 for r in results if r.get("result", {}).get("success")),
            "failed": sum(1 for r in results if not r.get("result", {}).get("success")),
            "results": results[:5],  # Limit output
        }

    async def _execute_step(self, step: dict) -> dict:
        """Execute a workflow step."""
        action = step.get("action", "")

        if action == "file_read":
            path = step.get("path", "")

            from pathlib import Path

            p = Path(path)

            try:
                content = p.read_text(encoding="utf-8")

                return {
                    "success": True,
                    "output": content[:500] + "...",
                    "type": "file_read",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        elif action == "file_write":
            path = step.get("path", "")
            content = step.get("content", "")

            from pathlib import Path

            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

            return {
                "success": True,
                "message": f"Written to {path}",
                "type": "file_write",
            }

        elif action == "execute_command":
            command = step.get("command", "")

            import subprocess

            try:
                result = subprocess.run(
                    ["bash", "-c", command], capture_output=True, text=True, timeout=30
                )

                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None,
                    "exit_code": result.returncode,
                }
            except subprocess.TimeoutExpired:
                return {"success": False, "error": "Command timed out"}
            except Exception as e:
                return {"success": False, "error": str(e)}

        else:
            return {"success": False, "error": f"Unknown step action: {action}"}
