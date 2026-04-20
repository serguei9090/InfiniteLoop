"""
Base Tools - Immutable Core Filesystem and Command Execution
PURPOSE: Provide safe, audited access to the workspace and system.
CONTRACT:
- read_file(path, mode): Returns skeleton, compressed, or full content.
- write_file(path, content): Securely writes to the workspace.
- execute_cmd(command): Runs shell commands within the sandbox.
"""

import platform
import asyncio
import os
import logging
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from typing import Dict

logger = logging.getLogger(__name__)


class BaseTools:
    def __init__(
        self,
        guard: WorkspaceGuard,
        context_engine: ContextEngine,
        evolution_engine: EvolutionEngine,
    ):
        self.guard = guard
        self.context = context_engine
        self.evolution = evolution_engine

    async def create_new_tool(self, name: str, code: str, schema: str) -> Dict:
        """
        Creates and registers a new dynamic tool.
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

    async def read_file(self, path: str, mode: str = "skeleton") -> Dict:
        """
        Reads content from a file in the workspace.

        Args:
            path: Relative path to the file.
            mode: 'skeleton' (headers), 'compressed' (no comments/docstrings), 'full' (raw).
        """
        try:
            safe_path = self.guard.secure_path(path, write=False)
            if mode == "skeleton":
                content = self.context.get_skeleton(safe_path)
            elif mode == "compressed":
                content = self.context.get_full_compressed(safe_path)
            else:
                content = await asyncio.to_thread(self._read_sync, safe_path)
            return {"success": True, "data": content, "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    def _read_sync(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    async def write_file(self, path: str, content: str) -> Dict:
        """
        Writes content to a file in the workspace.

        Args:
            path: Relative path to the file.
            content: The string content to write.
        """
        try:
            logger.debug(f"DEBUG: write_file called with {path}")
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

    async def delete_file(self, path: str) -> Dict:
        """
        Moves a file to the system's .trash folder.
        """
        try:
            self.guard.safe_delete(path)
            return {
                "success": True,
                "data": f"Successfully moved {path} to .trash",
                "error": None,
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def create_folder(self, path: str) -> Dict:
        """
        Creates a new folder in the workspace.
        """
        try:
            logger.debug(f"DEBUG: create_folder called with {path}")
            safe_path = self.guard.secure_path(path, write=True)
            await asyncio.to_thread(os.makedirs, safe_path, exist_ok=True)
            return {
                "success": True,
                "data": f"Successfully created folder {path}",
                "error": None,
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def execute_cmd(self, command: str) -> Dict:
        """
        Executes a shell command in the workspace root.
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

    async def glob_search(self, pattern: str) -> Dict:
        """
        Find files in the workspace matching a glob pattern.
        """
        try:
            import glob
            # Only search within the workspace root
            search_path = str(self.guard.root / pattern)
            results = glob.glob(search_path, recursive=True)
            # Make paths relative to root for the output
            rel_results = [os.path.relpath(p, str(self.guard.root)) for p in results]
            return {"success": True, "data": rel_results, "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def grep_search(self, query: str, path: str = ".") -> Dict:
        """
        Search for a string pattern in files.
        """
        try:
            safe_path = self.guard.secure_path(path, write=False)
            if platform.system() == "Windows":
                # PowerShell Select-String
                cmd = f'powershell.exe -Command "Get-ChildItem -Path \'{safe_path}\' -Recurse -File | Select-String -Pattern \'{query}\'"'
            else:
                # Unix grep
                cmd = f'grep -rn "{query}" "{safe_path}"'

            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.guard.root,
            )
            stdout, stderr = await process.communicate()

            return {
                "success": True,
                "data": stdout.decode(),
                "error": stderr.decode() if stderr else "",
            }
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}

    async def web_fetch(self, url: str) -> Dict:
        """
        Fetch content from a given URL.
        """
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True, timeout=10.0)
                response.raise_for_status()
                return {"success": True, "data": response.text, "error": None}
        except Exception as e:
            return {"success": False, "data": "", "error": str(e)}
