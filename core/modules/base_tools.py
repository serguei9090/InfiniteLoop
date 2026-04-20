import platform
import asyncio
import os
import logging
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine

logger = logging.getLogger(__name__)


class BaseTools:
    """
    Standard toolset for the IMMUTABLE CORE environment.
    Provides safe filesystem and system command execution.
    Compatible with Google ADK 2.0 (supports async).
    """

    def __init__(
        self,
        guard: WorkspaceGuard,
        context_engine: ContextEngine,
        evolution_engine: EvolutionEngine,
    ):
        self.guard = guard
        self.context = context_engine
        self.evolution = evolution_engine

    async def create_new_tool(self, name: str, code: str, schema: str) -> dict:
        """
        Creates and registers a new dynamic tool.

        Args:
            name: Unique name for the tool.
            code: Python code implementation.
            schema: JSON schema string for the tool's arguments.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            result = self.evolution.validate_and_register(name, code, schema)
            return {
                "success": result["success"],
                "data": result.get("message", ""),
                "error": result.get("error"),
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def read_file(self, path: str, mode: str = "skeleton") -> dict:
        """
        Reads content from a file in the workspace.

        Args:
            path: Relative path to the file.
            mode: 'skeleton' for high-level structure, 'full' for exact code.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            safe_path = self.guard.secure_path(path, write=False)
            if mode == "skeleton":
                content = self.context.get_skeleton(safe_path)
            else:
                content = await asyncio.to_thread(self._read_sync, safe_path)
            return {"success": True, "data": content, "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def _read_sync(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    async def write_file(self, path: str, content: str) -> dict:
        """
        Writes content to a file in the workspace.

        Args:
            path: Relative path to the file.
            content: The string content to write.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            print(f"DEBUG: write_file called with {path}")
            safe_path = self.guard.secure_path(path, write=True)
            # Ensure parent directories exist
            await asyncio.to_thread(os.makedirs, safe_path.parent, exist_ok=True)
            await asyncio.to_thread(self._write_sync, safe_path, content)
            return {
                "success": True,
                "data": f"Successfully wrote to {path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Write Error: {e}")
            return {"success": False, "data": "", "error": str(e)}

    def _write_sync(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    async def delete_file(self, path: str) -> dict:
        """
        Moves a file to the system's .trash folder.

        Args:
            path: Relative path to the file.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            # We use the existing guard method for now
            self.guard.safe_delete(path)
            return {
                "success": True,
                "data": f"Successfully moved {path} to .trash",
                "error": None,
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def create_folder(self, path: str) -> dict:
        """
        Creates a new folder in the workspace.

        Args:
            path: Relative path to the folder.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            print(f"DEBUG: create_folder called with {path}")
            safe_path = self.guard.secure_path(path, write=True)
            await asyncio.to_thread(os.makedirs, safe_path, exist_ok=True)
            return {
                "success": True,
                "data": f"Successfully created folder {path}",
                "error": None,
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def execute_cmd(self, command: str) -> dict:
        """
        Executes a shell command in the workspace root.

        Args:
            command: The exact shell command to run.

        Returns:
            A dict with 'success', 'data' (stdout), and 'error' (stderr).
        """
        try:
            destructive_patterns = ["rm ", "del ", "Remove-Item", "rd ", "rmdir"]
            if any(pattern in command.lower() for pattern in destructive_patterns):
                return {
                    "success": False,
                    "data": "",
                    "error": "Security Alert: Direct deletion via execute_cmd is forbidden.",
                }

            if platform.system() == "Windows":
                # Ensure powershell usage
                full_command = f'powershell.exe -Command "{command}"'
            else:
                full_command = command

            process = await asyncio.create_subprocess_shell(
                full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.guard.root,
            )
            stdout, stderr = await process.communicate()

            success = process.returncode == 0
            return {
                "success": success,
                "data": stdout.decode(),
                "error": stderr.decode() if not success else "",
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}
