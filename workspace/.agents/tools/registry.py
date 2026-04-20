"""
Tool Registry System
Centralized tool registration and loading system.
"""

import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Any


class ToolRegistry:
    """
    Centralized tool registry for managing all tools.
    
    Capabilities:
    - Register tools dynamically
    - Load tools from organized folders
    - Hot-load new tools without restart
    - Tool discovery and listing
    """
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.tool_categories: Dict[str, List[str]] = {
            "backend": [],
            "ui": [],
            "scripts": [],
            "api": []
        }
        self._load_path = Path(__file__).parent
    
    def register(self, tool: Any) -> None:
        """Register a tool."""
        name = tool.name if hasattr(tool, "name") else tool.__class__.__name__
        self.tools[name] = tool
        
        # Categorize the tool
        category = tool.category if hasattr(tool, "category") else "backend"
        if category not in self.tool_categories:
            self.tool_categories[category] = []
        self.tool_categories[category].append(name)
    
    def unregister(self, name: str) -> bool:
        """Unregister a tool."""
        if name in self.tools:
            del self.tools[name]
            return True
        return False
    
    def get_tool(self, name: str) -> Any:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools."""
        result = []
        for name, tool in self.tools.items():
            info = {
                "name": name,
                "description": tool.description if hasattr(tool, "description") else "",
                "category": tool.category if hasattr(tool, "category") else "backend"
            }
            result.append(info)
        return result
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get tools in a category."""
        return self.tool_categories.get(category, [])
    
    def load_from_folder(self, folder_path: Path) -> Dict[str, Any]:
        """Load all tools from a folder recursively."""
        loaded = {
            "success": True,
            "loaded": 0,
            "failed": 0,
            "tools": []
        }
        
        if not folder_path.exists():
            return loaded
        
        for py_file in folder_path.rglob("*.py"):
            # Skip __init__.py and test files
            if "__init__" in py_file.name or "test_" in py_file.name:
                continue
            
            try:
                module_name = py_file.stem
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find classes that look like tools (have name attribute)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if hasattr(attr, "name") and callable(attr):
                        self.register(attr())
                        loaded["loaded"] += 1
                        loaded["tools"].append({
                            "name": attr.name,
                            "class": attr.__class__.__name__
                        })
                        
            except Exception as e:
                loaded["failed"] += 1
        
        return loaded
    
    def hot_load(self, category: str) -> Dict[str, Any]:
        """Hot-load tools from a category folder without restart."""
        category_path = self._load_path / category
        
        if not category_path.exists():
            return {
                "success": False,
                "error": f"Category folder not found: {category}"
            }
        
        return self.load_from_folder(category_path)
    
    def hot_load_all(self) -> Dict[str, Any]:
        """Hot-load all tools from all categories."""
        results = {}
        for category in self.tool_categories.keys():
            results[category] = self.hot_load(category)
        return results
    
    def discover_tools(self) -> Dict[str, Any]:
        """Discover and load all available tools."""
        results = {
            "success": True,
            "categories": {},
            "total_loaded": 0
        }
        
        for category in self.tool_categories.keys():
            category_path = self._load_path / category
            if category_path.exists():
                loaded = self.load_from_folder(category_path)
                results["categories"][category] = loaded
        
        return results


# Global registry instance
registry = ToolRegistry()
