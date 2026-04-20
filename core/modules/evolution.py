"""
Evolution Engine - Dynamic Tool Synthesis and Validation
PURPOSE: Allow the agent to create and register new Python tools.
CONTRACT:
- validate_and_register(name, code, schema): Sanitizes, tests, and registers a tool.
- get_tool_descriptions(): Returns a summary of all active tools.
"""

import json
import ast
import subprocess
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class EvolutionEngine:
    def __init__(self, dynamic_tools_dir: str):
        self.tools_dir = Path(dynamic_tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.registered_tools: Dict[str, Dict[str, Any]] = {}

    def validate_and_register(
        self, name: str, code: str, schema_json: str
    ) -> Dict[str, Any]:
        """
        Validate syntax, security, and runtime of a new tool.
        """
        try:
            # 1. Syntax Pass
            ast.parse(code)

            # 2. Schema Compliance
            schema = json.loads(schema_json)
            if not all(key in schema for key in ["description", "properties"]):
                return {
                    "success": False,
                    "error": "Schema missing 'description' or 'properties'",
                }

            # 3. Security Scan (AST level)
            root = ast.parse(code)
            for node in ast.walk(root):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ["shutil", "subprocess"]:
                            return {
                                "success": False,
                                "error": f"Illegal import detected: {alias.name}",
                            }
                if isinstance(node, ast.ImportFrom):
                    if node.module in ["shutil", "subprocess"]:
                        return {
                            "success": False,
                            "error": f"Illegal import detected: {node.module}",
                        }

            # 4. Persistence
            tool_dir = self.tools_dir / name
            tool_dir.mkdir(parents=True, exist_ok=True)

            # Initialize uv project (if not exists)
            if not (tool_dir / "pyproject.toml").exists():
                subprocess.run(
                    ["uv", "init", "--lib"], cwd=tool_dir, capture_output=True
                )

            tool_path = tool_dir / "src" / f"{name}.py"
            schema_path = tool_dir / f"{name}.json"

            with open(tool_path, "w", encoding="utf-8") as f:
                f.write(code)
            with open(schema_path, "w", encoding="utf-8") as f:
                f.write(schema_json)

            # 5. Runtime Verification
            verify_cmd = (
                f"import sys; sys.path.append('src'); import {name}; print('OK')"
            )
            result = subprocess.run(
                ["uv", "run", "python", "-c", verify_cmd],
                cwd=tool_dir,
                capture_output=True,
                text=True,
            )

            if "OK" not in result.stdout:
                return {
                    "success": False,
                    "error": f"Tool dry-run failed: {result.stderr}",
                }

            # 6. Registration
            self.registered_tools[name] = {"path": str(tool_path), "schema": schema}

            return {
                "success": True,
                "message": f"Tool '{name}' successfully evolved and registered.",
            }

        except Exception as e:
            logger.error(f"Evolution Failure: {e}")
            return {"success": False, "error": f"Validation failed: {str(e)}"}

    def get_tool_descriptions(self) -> str:
        descriptions = []
        for name, info in self.registered_tools.items():
            desc = info["schema"].get("description", "No description")
            descriptions.append(f"- {name}: {desc}")
        return "\n".join(descriptions)
