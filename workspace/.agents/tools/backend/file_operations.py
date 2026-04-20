"""
File Operations Tool - Backend Category
Handles file read, write, create, edit operations.
"""

from pathlib import Path


class FileOperationsTool:
    """
    Tool for file system operations.

    Capabilities:
    - Read files
    - Write files
    - Create folders
    - Edit files (search/replace)
    - Delete files
    - List directory contents
    """

    name = "file_operations"
    description = "Perform file system operations including read, write, create, edit files and create folders"
    category = "backend"

    def __init__(self):
        self.operations_count = 0

    async def execute(self, args: dict) -> dict:
        """Execute file operation based on action type."""
        action = args.get("action", "")

        if action == "read":
            return await self._read_file(args)
        elif action == "write":
            return await self._write_file(args)
        elif action == "create_folder":
            return await self._create_folder(args)
        elif action == "edit":
            return await self._edit_file(args)
        elif action == "delete":
            return await self._delete_file(args)
        elif action == "list":
            return await self._list_directory(args)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}

    async def _read_file(self, args: dict) -> dict:
        """Read a file."""
        path = Path(args.get("path", ""))

        if not path.exists():
            return {"success": False, "error": f"File not found: {path}"}

        try:
            content = path.read_text(encoding="utf-8")
            self.operations_count += 1

            return {
                "success": True,
                "output": content,
                "operation": "read",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _write_file(self, args: dict) -> dict:
        """Write to a file."""
        path = Path(args.get("path", ""))
        content = args.get("content", "")

        try:
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(content, encoding="utf-8")
            self.operations_count += 1

            return {
                "success": True,
                "message": f"Written to {path}",
                "operation": "write",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _create_folder(self, args: dict) -> dict:
        """Create a folder."""
        path = Path(args.get("path", ""))

        try:
            path.mkdir(parents=True, exist_ok=True)
            self.operations_count += 1

            return {
                "success": True,
                "message": f"Created folder: {path}",
                "operation": "create_folder",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _edit_file(self, args: dict) -> dict:
        """Edit a file using search/replace."""
        path = Path(args.get("path", ""))
        search = args.get("search", "")
        replace = args.get("replace", "")

        if not path.exists():
            return {"success": False, "error": f"File not found: {path}"}

        try:
            content = path.read_text(encoding="utf-8")

            # Perform search/replace
            new_content = content.replace(search, replace)

            # Write back if changed
            if new_content != content:
                path.write_text(new_content, encoding="utf-8")
                self.operations_count += 1

            return {
                "success": True,
                "message": f"Edited {path}",
                "operation": "edit",
                "search": search,
                "replace": replace,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _delete_file(self, args: dict) -> dict:
        """Delete a file."""
        path = Path(args.get("path", ""))

        if not path.exists():
            return {"success": False, "error": f"File not found: {path}"}

        try:
            path.unlink()
            self.operations_count += 1

            return {
                "success": True,
                "message": f"Deleted: {path}",
                "operation": "delete",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _list_directory(self, args: dict) -> dict:
        """List directory contents."""
        path = Path(args.get("path", "."))

        try:
            items = [str(p.relative_to(path)) for p in path.iterdir()]

            return {
                "success": True,
                "output": "\n".join(items),
                "operation": "list",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
