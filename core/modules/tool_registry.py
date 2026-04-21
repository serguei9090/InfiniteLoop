"""
Tool Registry System - Orchestrator Brain Core
Manages tool registration, hot-loading, and auto-adaptation.
"""

import json
import importlib
import importlib.util
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
import time

logger = logging.getLogger(__name__)


@dataclass
class ToolDefinition:
    """Represents a registered tool definition."""

    name: str
    description: str
    function: Optional[Callable] = None
    module_path: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    is_dynamic: bool = False
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    enabled: bool = True


class ToolRegistry:
    """
    Central registry for all tools with hot-loading and auto-adaptation.

    Features:
    - Hot-load new tools without restart
    - Category-based organization (backend, ui, scripts, api)
    - Tool lifecycle management
    - Auto-adaptation tracking
    """

    def __init__(self, workspace_root: str = "./workspace"):
        self.workspace_root = Path(workspace_root).resolve()
        self.tools_dir = self.workspace_root / ".agents" / "tools"
        self.tools_dir.mkdir(parents=True, exist_ok=True)

        # Category directories
        self.categories = {
            "backend": self.tools_dir / "backend",
            "ui": self.tools_dir / "ui",
            "scripts": self.tools_dir / "scripts",
            "api": self.tools_dir / "api",
        }

        for category in self.categories.values():
            category.mkdir(parents=True, exist_ok=True)

        # Tool storage
        self._tools: Dict[str, ToolDefinition] = {}
        self._lock = asyncio.Lock()

        # Auto-adaptation tracking
        self.adaptation_log: List[Dict[str, Any]] = []
        self.hot_load_count = 0

        # Instructions file
        self.instructions_path = self.workspace_root / ".agents" / "instructions.json"

        # Load initial instructions
        self._load_instructions()

    def _load_instructions(self):
        """Load agent instructions from file."""
        if self.instructions_path.exists():
            try:
                with open(self.instructions_path, "r") as f:
                    instructions = json.load(f)
                    logger.info(f"Loaded {len(instructions)} agent instructions")
            except Exception as e:
                logger.warning(f"Failed to load instructions: {e}")

    def save_instructions(self, instructions: List[Dict[str, Any]]):
        """Save agent instructions."""
        self.instructions_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.instructions_path, "w") as f:
            json.dump(instructions, f, indent=2)
        logger.info(f"Saved {len(instructions)} agent instructions")

    async def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        schema: Optional[Dict[str, Any]] = None,
        category: str = "backend",
        is_dynamic: bool = False,
    ) -> Dict[str, Any]:
        """
        Register a new tool with hot-loading capability.

        Args:
            name: Unique tool name
            description: Tool description for LLM context
            code: Python code for the tool
            schema: JSON Schema for tool arguments
            category: Category (backend, ui, scripts, api)
            is_dynamic: Whether this is a dynamically created tool

        Returns:
            Registration result dict
        """
        async with self._lock:
            try:
                # Check if tool already exists
                if name in self._tools:
                    return {
                        "success": False,
                        "error": f"Tool '{name}' is already registered",
                        "tool_path": None,
                        "schema_path": None,
                    }

                # Create category directory if needed
                category_dir = self.categories.get(category, self.categories["backend"])
                category_dir.mkdir(parents=True, exist_ok=True)

                # Save tool code
                tool_file = category_dir / f"{name}.py"
                with open(tool_file, "w") as f:
                    f.write(code)

                # Save schema if provided
                if schema:
                    schema_file = category_dir / f"{name}.json"
                    with open(schema_file, "w") as f:
                        json.dump(schema, f, indent=2)

                # Create tool definition
                tool_def = ToolDefinition(
                    name=name,
                    description=description,
                    module_path=str(tool_file),
                    schema=schema,
                    is_dynamic=is_dynamic,
                )

                self._tools[name] = tool_def

                # Log adaptation event
                self.adaptation_log.append(
                    {
                        "event": "tool_registered",
                        "name": name,
                        "category": category,
                        "timestamp": time.time(),
                        "is_dynamic": is_dynamic,
                    }
                )

                logger.info(f"Registered tool: {name} (category: {category})")

                return {
                    "success": True,
                    "message": f"Tool '{name}' registered successfully",
                    "tool_path": str(tool_file),
                    "schema_path": str(schema_file) if schema else None,
                }

            except Exception as e:
                logger.error(f"Failed to register tool {name}: {e}")
                return {"success": False, "error": str(e)}

    async def hot_load_tool(self, name: str) -> Dict[str, Any]:
        """
        Hot-load a tool without restarting the application.

        Args:
            name: Tool name to load

        Returns:
            Loading result dict
        """
        async with self._lock:
            try:
                if name not in self._tools:
                    return {
                        "success": False,
                        "error": f"Tool '{name}' not found in registry",
                    }

                tool_def = self._tools[name]
                module_path = Path(tool_def.module_path)

                # Import the module dynamically
                module_name = f"dynamic_tools.{name}"

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Check for run function or main entry point
                    run_func = getattr(module, "run", None)
                    main_func = getattr(module, "main", None)

                    if run_func:
                        tool_def.function = run_func
                    elif main_func:
                        tool_def.function = lambda **kwargs: asyncio.run(
                            main_func(**kwargs)
                        )

                self.hot_load_count += 1
                tool_def.last_used = time.time()

                # Log hot-load event
                self.adaptation_log.append(
                    {
                        "event": "hot_loaded",
                        "name": name,
                        "timestamp": time.time(),
                        "hot_load_count": self.hot_load_count,
                    }
                )

                logger.info(
                    f"Hot-loaded tool: {name} (total hot-loads: {self.hot_load_count})"
                )

                return {
                    "success": True,
                    "message": f"Tool '{name}' hot-loaded successfully",
                    "function": tool_def.function is not None,
                }

            except Exception as e:
                logger.error(f"Failed to hot-load tool {name}: {e}")
                return {"success": False, "error": str(e)}

    async def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered tools, optionally filtered by category."""
        tools_list = []

        for name, tool_def in self._tools.items():
            if category and tool_def.module_path:
                module_path = Path(tool_def.module_path)
                tool_category = module_path.parent.name or "backend"

                if category == tool_category:
                    tools_list.append(
                        {
                            "name": name,
                            "description": tool_def.description,
                            "category": tool_category,
                            "is_dynamic": tool_def.is_dynamic,
                            "created_at": tool_def.created_at,
                            "last_used": tool_def.last_used,
                        }
                    )
            else:
                tools_list.append(
                    {
                        "name": name,
                        "description": tool_def.description,
                        "category": (module_path.parent.name or "backend")
                        if (module_path := Path(tool_def.module_path))
                        else "backend",
                        "is_dynamic": tool_def.is_dynamic,
                        "created_at": tool_def.created_at,
                        "last_used": tool_def.last_used,
                    }
                )

        return tools_list

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name."""
        return self._tools.get(name)

    async def enable_tool(self, name: str) -> Dict[str, Any]:
        """Enable a registered tool."""
        async with self._lock:
            if name in self._tools:
                self._tools[name].enabled = True
                self.adaptation_log.append({
                    "event": "tool_enabled",
                    "name": name,
                    "timestamp": time.time()
                })
                logger.info(f"Enabled tool: {name}")
                return {"success": True, "message": f"Tool '{name}' enabled successfully"}
            return {"success": False, "error": f"Tool '{name}' not found"}

    async def disable_tool(self, name: str) -> Dict[str, Any]:
        """Disable a registered tool."""
        async with self._lock:
            if name in self._tools:
                self._tools[name].enabled = False
                self.adaptation_log.append({
                    "event": "tool_disabled",
                    "name": name,
                    "timestamp": time.time()
                })
                logger.info(f"Disabled tool: {name}")
                return {"success": True, "message": f"Tool '{name}' disabled successfully"}
            return {"success": False, "error": f"Tool '{name}' not found"}

    async def remove_tool(self, name: str) -> Dict[str, Any]:
        """Remove a tool from the registry."""
        async with self._lock:
            if name in self._tools:
                del self._tools[name]

                # Clean up files
                for category_dir in self.categories.values():
                    tool_file = category_dir / f"{name}.py"
                    schema_file = category_dir / f"{name}.json"

                    if tool_file.exists():
                        tool_file.unlink()
                    if schema_file.exists():
                        schema_file.unlink()

                # Log removal
                self.adaptation_log.append(
                    {"event": "tool_removed", "name": name, "timestamp": time.time()}
                )

                logger.info(f"Removed tool: {name}")

                return {
                    "success": True,
                    "message": f"Tool '{name}' removed successfully",
                }

            return {"success": False, "error": f"Tool '{name}' not found"}

    def get_adaptation_stats(self) -> Dict[str, Any]:
        """Get auto-adaptation statistics."""
        return {
            "total_tools": len(self._tools),
            "hot_load_count": self.hot_load_count,
            "adaptation_events": len(self.adaptation_log),
            "categories": {
                cat: len(
                    [
                        t
                        for t in self._tools.values()
                        if (Path(t.module_path) or Path()).parent.name == cat
                    ]
                )
                for cat in self.categories.keys()
            },
            "recent_events": self.adaptation_log[-10:] if self.adaptation_log else [],
        }

    def get_instructions(self) -> List[Dict[str, Any]]:
        """Get loaded agent instructions."""
        try:
            with open(self.instructions_path, "r") as f:
                return json.load(f)
        except Exception:
            return []

    async def save_adaptation_log(self):
        """Save adaptation log to file."""
        log_path = self.workspace_root / ".agents" / "adaptation_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, "w") as f:
            json.dump(self.adaptation_log, f, indent=2, default=str)

    def get_tool_descriptions(self) -> str:
        """Get formatted tool descriptions for system prompt."""
        descriptions = []
        for name, tool_def in self._tools.items():
            desc = tool_def.description or f"Tool: {name}"
            if tool_def.schema:
                props = ", ".join(tool_def.schema.get("properties", {}).keys())
                desc += f" (args: [{props}])"
            descriptions.append(f"- {name}: {desc}")
        return (
            "\n".join(descriptions)
            if descriptions
            else "No custom tools registered yet."
        )
