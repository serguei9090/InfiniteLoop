import subprocess
import platform
from typing import Dict, Any, Optional
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine


class BaseTools:
    """
    Standard toolset for the IMMUTABLE CORE environment.
    Provides safe filesystem and system command execution.
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

    def create_new_tool(self, name: str, code: str, schema: str) -> dict:
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
                "error": result.get("error")
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def read_file(self, path: str, mode: str = "skeleton") -> dict:
        """
        Reads content from a file in the workspace.

        Args:
            path: Relative path to the file.
            mode: 'skeleton' for high-level structure, 'full' for exact code.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            safe_path = self.guard.secure_path(path)
            if mode == "skeleton":
                content = self.context.get_skeleton(safe_path)
            else:
                with open(safe_path, "r", encoding="utf-8") as f:
                    content = f.read()
            return {"success": True, "data": content, "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def write_file(self, path: str, content: str) -> dict:
        """
        Writes content to a file in the workspace.

        Args:
            path: Relative path to the file.
            content: The string content to write.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            safe_path = self.guard.secure_path(path)
            # Ensure parent directories exist
            safe_path.parent.mkdir(parents=True, exist_ok=True)
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "data": f"Successfully wrote to {path}", "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def delete_file(self, path: str) -> dict:
        """
        Moves a file to the system's .trash folder.

        Args:
            path: Relative path to the file.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            self.guard.safe_delete(path)
            return {"success": True, "data": f"Successfully moved {path} to .trash", "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def create_folder(self, path: str) -> dict:
        """
        Creates a new folder in the workspace.

        Args:
            path: Relative path to the folder.

        Returns:
            A dict with 'success', 'data', and 'error' keys.
        """
        try:
            safe_path = self.guard.secure_path(path)
            safe_path.mkdir(parents=True, exist_ok=True)
            return {"success": True, "data": f"Successfully created folder {path}", "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def execute_cmd(self, command: str) -> dict:
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
                    "error": "Security Alert: Direct deletion via execute_cmd is forbidden."
                }

            if platform.system() == "Windows":
                full_command = f"powershell.exe -Command \"{command}\""
            else:
                full_command = command

            process = subprocess.run(
                full_command,
                shell=True,
                cwd=self.guard.root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            data = process.stdout
            error = process.stderr if process.returncode != 0 else None
            return {
                "success": process.returncode == 0,
                "data": data,
                "error": error or (f"Exit code: {process.returncode}" if process.returncode != 0 else None)
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}
