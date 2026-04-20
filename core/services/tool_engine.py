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
            # Try to find all JSON-like blocks and take the first valid one
            import re

            json_blocks = re.findall(
                r"```json\s*(\{.*?\})\s*```", tool_call_json, re.DOTALL
            )
            if not json_blocks:
                json_blocks = re.findall(r"(\{.*?\})", tool_call_json, re.DOTALL)

            if json_blocks:
                clean_json = json_blocks[0]
            else:
                clean_json = tool_call_json.strip()

            data = json.loads(clean_json, strict=False)
            tool_name = data.get("tool")
            args = data.get("args", {})

            if tool_name == "read_file":
                return await self.tools.read_file(**args)
            elif tool_name == "write_file":
                return await self.tools.write_file(**args)
            elif tool_name == "execute_cmd":
                return await self.tools.execute_cmd(**args)
            elif tool_name == "delete_file":
                return await self.tools.delete_file(**args)
            elif tool_name == "create_folder":
                return await self.tools.create_folder(**args)
            elif tool_name == "create_new_tool":
                return await self.tools.create_new_tool(**args)

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
