"""
Batch Operations Tool - Scripts Category
Handles batch processing, file operations on multiple files, and bulk tasks.
"""


class BatchOperationsTool:
    """
    Tool for batch operations and bulk processing.
    
    Capabilities:
    - Process multiple files at once
    - Bulk file operations
    - Parallel task execution
    - Batch data transformations
    """
    
    name = "batch_operations"
    description = "Perform batch operations on multiple files, bulk processing, and parallel tasks"
    category = "scripts"
    
    def __init__(self):
        self.batch_count = 0
    
    async def execute(self, args: dict) -> dict:
        """Execute batch operation."""
        action = args.get("action", "")
        
        if action == "process_files":
            return await self._process_files(args)
        elif action == "bulk_rename":
            return await self._bulk_rename(args)
        elif action == "parallel_execute":
            return await self._parallel_execute(args)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
    
    async def _process_files(self, args: dict) -> dict:
        """Process multiple files."""
        file_pattern = args.get("pattern", "*.txt")
        operation = args.get("operation", "read")
        
        import glob
        
        # Find matching files
        files = glob.glob(file_pattern)
        
        if not files:
            return {
                "success": False,
                "error": f"No files found matching pattern: {file_pattern}"
            }
        
        self.batch_count += 1
        
        results = []
        for file_path in files:
            try:
                result = await self._process_single_file(file_path, operation)
                results.append({
                    "file": file_path,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "file": file_path,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "operation": "process_files",
            "pattern": file_pattern,
            "files_processed": len(files),
            "results": results
        }
    
    async def _process_single_file(self, path: str, operation: str) -> dict:
        """Process a single file."""
        from pathlib import Path
        
        p = Path(path)
        
        if operation == "read":
            try:
                content = p.read_text(encoding="utf-8")
                return {
                    "success": True,
                    "output": content[:1000] + "...",  # Limit output
                    "lines": len(content.splitlines())
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif operation == "count_lines":
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
                return {
                    "success": True,
                    "output": len(lines),
                    "type": "line_count"
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif operation == "count_words":
            try:
                content = p.read_text(encoding="utf-8")
                words = len(content.split())
                return {
                    "success": True,
                    "output": words,
                    "type": "word_count"
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}"
            }
    
    async def _bulk_rename(self, args: dict) -> dict:
        """Bulk rename files."""
        pattern = args.get("pattern", "*.txt")
        new_name = args.get("new_name", "")
        
        import glob
        
        files = glob.glob(pattern)
        
        if not files:
            return {
                "success": False,
                "error": f"No files found matching pattern: {pattern}"
            }
        
        self.batch_count += 1
        
        renamed = []
        for file_path in files:
            try:
                new_path = Path(new_name) / Path(file_path).name if new_name else file_path
                Path(file_path).rename(new_path)
                renamed.append(str(file_path))
            except Exception as e:
                pass  # Skip failed renames
        
        return {
            "success": True,
            "operation": "bulk_rename",
            "pattern": pattern,
            "new_name": new_name,
            "files_renamed": len(renamed),
            "renamed_files": renamed[:10]  # Limit output
        }
    
    async def _parallel_execute(self, args: dict) -> dict:
        """Execute tasks in parallel."""
        tasks = args.get("tasks", [])
        
        if not tasks:
            return {
                "success": False,
                "error": "No tasks provided"
            }
        
        self.batch_count += 1
        
        # Execute tasks (simplified - in real implementation would use asyncio.gather)
        results = []
        for task in tasks:
            try:
                result = await self._execute_task(task)
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "operation": "parallel_execute",
            "tasks_count": len(tasks),
            "successful": sum(1 for r in results if r.get("success")),
            "failed": sum(1 for r in results if not r.get("success")),
            "results": results[:5]  # Limit output
        }
    
    async def _execute_task(self, task: dict) -> dict:
        """Execute a single task."""
        task_type = task.get("type", "")
        
        if task_type == "file_read":
            path = task.get("path", "")
            return await self._process_single_file(path, "read")
        
        elif task_type == "file_write":
            path = task.get("path", "")
            content = task.get("content", "")
            
            from pathlib import Path
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            
            return {
                "success": True,
                "message": f"Written to {path}",
                "type": "file_write"
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown task type: {task_type}"
            }
