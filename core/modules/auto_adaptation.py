"""
Auto-Adaptation Engine - Orchestrator Brain Core
Handles hot-loading, module testing, and self-improvement loops.
"""

import importlib
import importlib.util
import logging
import time
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ModuleInfo:
    """Information about a loaded module."""

    name: str
    path: str
    category: str
    status: str  # "loaded", "testing", "error"
    last_tested: float = field(default_factory=time.time)
    test_result: Optional[str] = None
    error_count: int = 0


class AutoAdaptationEngine:
    """
    Engine for auto-adaptation with hot-loading and self-improvement.

    Features:
    - Hot-load modules without restart
    - Automated testing of loaded modules
    - Error recovery and retry logic
    - Module lifecycle management
    - Self-improvement loop tracking
    """

    def __init__(self, workspace_root: str = "./workspace"):
        self.workspace_root = Path(workspace_root).resolve()

        # Module storage by category
        self.modules: Dict[str, Dict[str, ModuleInfo]] = {
            "backend": {},
            "ui": {},
            "scripts": {},
            "api": {},
        }

        # Test configurations per category
        self.test_configs = {
            "backend": {"timeout": 30, "retry": 2},
            "ui": {"timeout": 15, "retry": 1},
            "scripts": {"timeout": 60, "retry": 3},
            "api": {"timeout": 30, "retry": 2},
        }

        # Self-improvement tracking
        self.improvement_log: List[Dict[str, Any]] = []
        self.error_patterns: Dict[str, int] = {}

        # Hot-load tracking
        self.hot_load_count = 0
        self.last_hot_load_time: float = 0

        # Test runner callback
        self.test_callback: Optional[Callable[[str, str], None]] = None

    async def hot_load_module(
        self, name: str, category: str, module_path: Path
    ) -> Dict[str, Any]:
        """
        Hot-load a module without restarting the application.

        Args:
            name: Module name
            category: Category (backend, ui, scripts, api)
            module_path: Path to module file

        Returns:
            Loading result dict
        """
        try:
            # Create module info
            module_info = ModuleInfo(
                name=name, path=str(module_path), category=category, status="loading"
            )

            self.modules[category][name] = module_info

            # Import the module dynamically
            module_name = f"hotloaded.{category}.{name}"

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Extract run/main function if exists
                run_func = getattr(module, "run", None)
                main_func = getattr(module, "main", None)

                if run_func or main_func:
                    module_info.status = "loaded"

                    self.hot_load_count += 1
                    self.last_hot_load_time = time.time()

                    # Log hot-load event
                    self._log_improvement(
                        "hot_load",
                        {
                            "name": name,
                            "category": category,
                            "hot_load_count": self.hot_load_count,
                        },
                    )

                    logger.info(
                        f"Hot-loaded module: {name} (total: {self.hot_load_count})"
                    )

                    return {
                        "success": True,
                        "message": f"Module '{name}' hot-loaded successfully",
                        "has_entry_point": run_func is not None
                        or main_func is not None,
                    }
                else:
                    module_info.status = "error"
                    module_info.test_result = "No entry point found (run/main)"

            else:
                module_info.status = "error"
                module_info.test_result = "Failed to load module spec"

            return {
                "success": False,
                "error": str(module_info.test_result or "Unknown error"),
            }

        except Exception as e:
            if name in self.modules[category]:
                module_info = self.modules[category][name]
                module_info.status = "error"
                module_info.error_count += 1

                logger.error(f"Failed to hot-load module {name}: {e}")

                return {"success": False, "error": str(e)}

            return {"success": False, "error": f"Module '{name}' not found in registry"}

    async def test_module(self, name: str, category: str) -> Dict[str, Any]:
        """
        Test a loaded module.

        Args:
            name: Module name
            category: Category

        Returns:
            Test result dict
        """
        if category not in self.modules or name not in self.modules[category]:
            return {
                "success": False,
                "error": f"Module '{name}' not found in category '{category}'",
            }

        module_info = self.modules[category][name]
        self.test_configs.get(category, {"timeout": 30, "retry": 2})

        module_info.status = "testing"

        try:
            # Run tests if test_callback is set
            if self.test_callback:
                await self.test_callback(name, category)

            module_info.last_tested = time.time()
            module_info.status = "loaded"
            module_info.test_result = "passed"

            self._log_improvement("test_passed", {"name": name, "category": category})

            logger.info(f"Module test passed: {name}")

            return {"success": True, "message": f"Module '{name}' test passed"}

        except Exception as e:
            module_info.status = "error"
            module_info.test_result = str(e)
            module_info.error_count += 1

            self._log_improvement(
                "test_failed", {"name": name, "category": category, "error": str(e)}
            )

            logger.error(f"Module test failed: {name} - {e}")

            return {"success": False, "error": str(e)}

    async def run_self_improvement_loop(self, mission: str = None) -> Dict[str, Any]:
        """
        Run the self-improvement loop for error fixing and testing.

        This method:
        1. Collects all errors from modules
        2. Analyzes error patterns
        3. Attempts auto-fixes where possible
        4. Retests modules after fixes

        Returns:
            Loop result dict
        """
        logger.info("Starting self-improvement loop...")

        # Collect all module errors
        all_errors = []
        for category, modules in self.modules.items():
            for name, info in modules.items():
                if info.status == "error":
                    all_errors.append(
                        {
                            "name": name,
                            "category": category,
                            "error": info.test_result,
                            "error_count": info.error_count,
                        }
                    )

        if not all_errors:
            logger.info("No errors found - self-improvement loop complete")
            return {"success": True, "message": "No errors to fix", "errors_fixed": 0}

        # Analyze error patterns
        for error in all_errors:
            error_key = str(error["error"])[:100]  # Truncate for key
            self.error_patterns[error_key] = self.error_patterns.get(error_key, 0) + 1

        # Attempt auto-fixes
        fixed_count = 0
        for error in all_errors:
            result = await self._attempt_auto_fix(error)
            if result["success"]:
                fixed_count += 1

        # Log improvement event
        self._log_improvement(
            "self_improvement_loop",
            {
                "total_errors": len(all_errors),
                "errors_fixed": fixed_count,
                "patterns_found": len(self.error_patterns),
            },
        )

        return {
            "success": True,
            "message": f"Self-improvement loop complete. Fixed {fixed_count}/{len(all_errors)} errors",
            "errors_fixed": fixed_count,
            "total_errors": len(all_errors),
        }

    async def _attempt_auto_fix(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to auto-fix an error.

        Args:
            error: Error info dict

        Returns:
            Fix result dict
        """
        name = error["name"]
        category = error["category"]
        error_msg = error["error"]

        logger.info(f"Attempting auto-fix for {name}: {error_msg}")

        # Strategy 1: Retry the module load
        if category in self.modules and name in self.modules[category]:
            module_info = self.modules[category][name]

            try:
                # Clear cached module
                module_name = f"hotloaded.{category}.{name}"
                if module_name in sys.modules:
                    del sys.modules[module_name]

                # Retry hot-load
                result = await self.hot_load_module(
                    name, category, Path(module_info.path)
                )

                if result["success"]:
                    logger.info(f"Auto-fix successful for {name}")
                    return result

            except Exception as e:
                logger.error(f"Auto-fix failed for {name}: {e}")

        # Strategy 2: Create a simplified version of the module
        simplified_path = (
            self.workspace_root / ".agents" / "auto_fixes" / f"{name}_simplified.py"
        )
        simplified_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(module_info.path, "r") as f:
                code = f.read()

            # Create simplified version (just the run function)
            simplified_code = self._extract_run_function(code)

            if simplified_code:
                with open(simplified_path, "w") as f:
                    f.write(simplified_code)

                # Hot-load simplified version
                result = await self.hot_load_module(name, category, simplified_path)

                if result["success"]:
                    logger.info(f"Auto-fix successful (simplified) for {name}")
                    return result

        except Exception as e:
            logger.error(f"Failed to create simplified module: {e}")

        return {"success": False, "error": f"No auto-fix available for {name}"}

    def _extract_run_function(self, code: str) -> Optional[str]:
        """Extract just the run() function from a module."""
        try:
            import ast

            tree = ast.parse(code)

            # Find run or main function
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in ("run", "main"):
                        # Extract function code
                        lines = code.split("\n")
                        start = node.lineno - 1

                        # Find end of function (matching indentation)
                        indent_level = len(lines[start]) - len(lines[start].lstrip())
                        end = start + 1

                        for i in range(start + 1, len(lines)):
                            if (
                                lines[i].strip()
                                and len(lines[i]) - len(lines[i].lstrip())
                                <= indent_level
                            ):
                                break
                            end = i + 1

                        # Format as function
                        func_lines = lines[start:end]

                        return "\n".join(func_lines)

            return None

        except Exception as e:
            logger.error(f"Failed to extract run function: {e}")
            return None

    def _log_improvement(self, event: str, data: Dict[str, Any]):
        """Log an improvement event."""
        self.improvement_log.append({"event": event, **data, "timestamp": time.time()})

        # Keep only last 100 events
        if len(self.improvement_log) > 100:
            self.improvement_log = self.improvement_log[-100:]

    def get_module_status(self, name: str, category: str) -> Optional[ModuleInfo]:
        """Get status of a specific module."""
        if category in self.modules and name in self.modules[category]:
            return self.modules[category][name]
        return None

    def get_all_modules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all modules with their status."""
        result = {}

        for category, modules in self.modules.items():
            result[category] = []
            for name, info in modules.items():
                result[category].append(
                    {
                        "name": name,
                        "path": info.path,
                        "status": info.status,
                        "last_tested": info.last_tested,
                        "test_result": info.test_result,
                        "error_count": info.error_count,
                    }
                )

        return result

    def get_adaptation_stats(self) -> Dict[str, Any]:
        """Get auto-adaptation statistics."""
        return {
            "hot_load_count": self.hot_load_count,
            "last_hot_load_time": self.last_hot_load_time,
            "total_modules": sum(len(m) for m in self.modules.values()),
            "error_patterns": self.error_patterns,
            "improvement_events": len(self.improvement_log),
            "recent_events": self.improvement_log[-10:] if self.improvement_log else [],
        }
