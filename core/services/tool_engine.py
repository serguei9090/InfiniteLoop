import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, Any
from modules.base_tools import BaseTools

logger = logging.getLogger(__name__)


class ToolEngine:
    def __init__(self, tools: BaseTools):
        self.tools = tools

    async def execute(self, tool_call_json: str) -> Dict[str, Any]:
        """
        Parses and executes a tool call.
        """
        try:
            # Enhanced JSON extraction
            import re
            json_match = re.search(r"(\{.*\})", tool_call_json, re.DOTALL)
            if json_match:
                clean_json = json_match.group(1)
            else:
                clean_json = tool_call_json.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json.split("```json", 1)[1].rsplit("```", 1)[0].strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json.split("```", 1)[1].rsplit("```", 1)[0].strip()

            data = json.loads(clean_json)
            tool_name = data.get("tool")
            args = data.get("args", {})

            if tool_name == "read_file":
                return self.tools.read_file(**args).to_dict()
            elif tool_name == "write_file":
                return self.tools.write_file(**args).to_dict()
            elif tool_name == "execute_cmd":
                return self.tools.execute_cmd(**args).to_dict()
            elif tool_name == "delete_file":
                return self.tools.delete_file(**args).to_dict()
            elif tool_name == "create_folder":
                return self.tools.create_folder(**args).to_dict()
            elif tool_name == "create_new_tool":
                return self.tools.create_new_tool(**args).to_dict()

            # Check for dynamic tools
            elif tool_name in self.tools.evolution.registered_tools:
                return self._execute_dynamic_tool(tool_name, args)

            else:
                return {
                    "success": False,
                    "data": "",
                    "error": f"Unknown tool: {tool_name}",
                }

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "data": "",
                "error": f"Invalid JSON format: {str(e)}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": "",
                "error": f"Tool Engine Error: {str(e)}",
            }

    def _execute_dynamic_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            tool_info = self.tools.evolution.registered_tools[name]
            tool_dir = Path(tool_info["path"]).parent.parent  # The uv project root

            # Prepare arguments as JSON string
            args_json = json.dumps(args)

            # Execute via uv run
            # The tool script is expected to have a if __name__ == "__main__": block that calls run()
            # Or we can use a wrapper
            exec_cmd = f"import sys; sys.path.append('src'); from {name} import run; import json; print(json.dumps(run(**json.loads(sys.argv[1]))))"

            result = subprocess.run(
                ["uv", "run", "python", "-c", exec_cmd, args_json],
                cwd=tool_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                try:
                    return {
                        "success": True,
                        "data": json.loads(result.stdout.strip()),
                        "error": None,
                    }
                except json.JSONDecodeError:
                    return {
                        "success": True,
                        "data": result.stdout.strip(),
                        "error": None,
                    }
            else:
                return {
                    "success": False,
                    "data": result.stdout,
                    "error": result.stderr or f"Exit code: {result.returncode}",
                }
        except Exception as e:
            return {
                "success": False,
                "data": "",
                "error": f"Dynamic Tool '{name}' execution failed: {str(e)}",
            }
