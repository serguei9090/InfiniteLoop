"""
Code Execution Tool - Backend Category
Handles code execution in sandboxed environment.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


class CodeExecutionTool:
    """
    Tool for executing code in a sandboxed environment.
    
    Capabilities:
    - Execute Python code
    - Run shell commands (with restrictions)
    - Create temporary files for code execution
    """
    
    name = "code_execution"
    description = "Execute code in a sandboxed environment including Python scripts and shell commands"
    category = "backend"
    
    def __init__(self):
        self.executions_count = 0
    
    async def execute(self, args: dict) -> dict:
        """Execute code based on language type."""
        language = args.get("language", "python")
        code = args.get("code", "")
        
        if language == "python":
            return await self._execute_python(code)
        elif language == "bash":
            return await self._execute_bash(code)
        else:
            return {
                "success": False,
                "error": f"Unsupported language: {language}"
            }
    
    async def _execute_python(self, code: str) -> dict:
        """Execute Python code."""
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute the Python code
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout
                )
                
                self.executions_count += 1
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None,
                    "exit_code": result.returncode
                }
            finally:
                # Clean up temporary file
                try:
                    Path(temp_file).unlink()
                except Exception:
                    pass
                    
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Code execution timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _execute_bash(self, code: str) -> dict:
        """Execute bash shell commands."""
        try:
            # Security check - only allow safe commands
            forbidden_patterns = ["rm -rf", "dd if=", "> /dev/", "mkfs"]
            
            for pattern in forbidden_patterns:
                if pattern.lower() in code.lower():
                    return {
                        "success": False,
                        "error": f"Command blocked for security reasons: {pattern}"
                    }
            
            result = subprocess.run(
                ["bash", "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
                shell=False
            )
            
            self.executions_count += 1
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
