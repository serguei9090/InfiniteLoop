import logging
import os
from typing import Dict, Any, List

from smolagents import Tool, CodeAgent, LiteLLMModel
from config import settings
from modules.base_tools import BaseTools

logger = logging.getLogger(__name__)


class SmolAgentWrapper:
    """Wraps the BaseTools into smolagents Tools and runs the CodeAgent."""

    def __init__(self, base_tools: BaseTools, workspace_root: str):
        self.base_tools = base_tools
        self.workspace_root = workspace_root

        # Configure model to use our litellm proxy
        proxy_url = os.environ.get("LITELLM_PROXY_URL", settings.litellm_proxy_url)
        api_key = os.environ.get("LITELLM_API_KEY", settings.litellm_api_key)

        self.model = LiteLLMModel(
            model_id="gemini/gemma-3-27b-it",  # routed through proxy
            api_base=proxy_url,
            api_key=api_key,
            max_tokens=4096,
        )
        self.agent = self._create_agent()

    def _create_agent(self) -> CodeAgent:
        tools = self._get_smol_tools()
        return CodeAgent(
            tools=tools,
            model=self.model,
            additional_authorized_imports=["os", "json", "pathlib", "re"],
            max_steps=10,
        )

    def _get_smol_tools(self) -> List[Tool]:
        """Convert BaseTools methods to SmolAgent Tools."""
        tools = []

        # Manually create tool classes that wrap BaseTools async methods
        # (SmolAgents expects synchronous tools by default, or we can use asyncio.run)

        class ExecuteBashTool(Tool):
            name = "execute_bash"
            description = "Executes a shell command in the workspace."
            inputs = {
                "command": {"type": "string", "description": "The command to run"}
            }
            output_type = "string"

            def __init__(self, base_tools):
                super().__init__()
                self.base_tools = base_tools

            def forward(self, command: str) -> str:
                import asyncio

                result = asyncio.run(self.base_tools.execute_bash(command))
                return str(result)

        class ReadFileTool(Tool):
            name = "read_file"
            description = "Reads a file from the workspace."
            inputs = {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to workspace",
                }
            }
            output_type = "string"

            def __init__(self, base_tools):
                super().__init__()
                self.base_tools = base_tools

            def forward(self, file_path: str) -> str:
                import asyncio

                result = asyncio.run(self.base_tools.read_file(file_path))
                return str(result)

        class WriteFileTool(Tool):
            name = "write_file"
            description = "Writes content to a file in the workspace."
            inputs = {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to workspace",
                },
                "content": {"type": "string", "description": "Content to write"},
            }
            output_type = "string"

            def __init__(self, base_tools):
                super().__init__()
                self.base_tools = base_tools

            def forward(self, file_path: str, content: str) -> str:
                import asyncio

                result = asyncio.run(self.base_tools.write_file(file_path, content))
                return str(result)

        class EditFileTool(Tool):
            name = "edit_file"
            description = (
                "Edits a file by replacing a search string with a replacement string."
            )
            inputs = {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to workspace",
                },
                "search_string": {
                    "type": "string",
                    "description": "Exact text to find",
                },
                "replacement_string": {
                    "type": "string",
                    "description": "Text to replace it with",
                },
            }
            output_type = "string"

            def __init__(self, base_tools):
                super().__init__()
                self.base_tools = base_tools

            def forward(
                self, file_path: str, search_string: str, replacement_string: str
            ) -> str:
                import asyncio

                result = asyncio.run(
                    self.base_tools.edit_file(
                        file_path, search_string, replacement_string
                    )
                )
                return str(result)

        tools.extend(
            [
                ExecuteBashTool(self.base_tools),
                ReadFileTool(self.base_tools),
                WriteFileTool(self.base_tools),
                EditFileTool(self.base_tools),
            ]
        )

        return tools

    async def run_task(
        self, task_description: str, target_file: str, verification: str
    ) -> Dict[str, Any]:
        """Execute a single atomic task using the code agent."""
        prompt = f"""
MISSION TASK: {task_description}

TARGET FILE: {target_file}

VERIFICATION STEP: {verification}

INSTRUCTIONS:
1. Use your read_file tool to inspect the target file or relevant context.
2. Use python code to plan the edits or use edit_file / write_file / execute_bash directly.
3. Finally, run the verification step using execute_bash to ensure success.
"""
        try:
            logger.info(f"Starting SmolAgent on task: {task_description[:50]}...")
            import asyncio

            # CodeAgent.run is sync, so we run it in a thread
            result = await asyncio.to_thread(self.agent.run, prompt)
            return {"success": True, "result": result}
        except Exception as e:
            logger.exception(f"SmolAgent Execution Error: {e}")
            return {"success": False, "error": str(e)}
