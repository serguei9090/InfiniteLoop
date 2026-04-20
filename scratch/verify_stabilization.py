import asyncio
import os
from pathlib import Path
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine
from modules.evolution import EvolutionEngine
from modules.base_tools import BaseTools


async def test_execute_cmd():
    project_root = Path(__file__).parent.parent.resolve()
    workspace_root = project_root / "workspace"
    workspace_root.mkdir(parents=True, exist_ok=True)

    guard = WorkspaceGuard(str(workspace_root))
    context_engine = ContextEngine()
    evolution = EvolutionEngine(str(workspace_root / ".agents" / "dynamic_tools"))
    tools = BaseTools(guard, context_engine, evolution)

    print(f"Testing execute_cmd in {workspace_root}")

    # Test 1: Simple dir/ls
    cmd = "dir" if os.name == "nt" else "ls"
    result = await tools.execute_cmd(cmd)
    print(f"Result 1 (success={result['success']}):\n{result['data'][:200]}...")

    # Test 2: Nested file creation and listing
    test_dir = "test/deep"
    await tools.create_folder(test_dir)
    await tools.write_file(f"{test_dir}/target.md", "# Target File")

    cmd = f"dir {test_dir}" if os.name == "nt" else f"ls {test_dir}"
    result = await tools.execute_cmd(cmd)
    print(f"Result 2 (success={result['success']}):\n{result['data']}")

    assert result["success"] is True
    assert "target.md" in result["data"]


if __name__ == "__main__":
    asyncio.run(test_execute_cmd())
