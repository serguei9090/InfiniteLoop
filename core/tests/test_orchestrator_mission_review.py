"""
Mission Review Tests - Comprehensive validation for IMMUTABLE CORE Orchestrator Brain
Tests all core capabilities including tool registry, auto-adaptation, file operations,
frontend connection, agent instructions loading, and self-improvement loops.
"""

import pytest
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.orchestrator_brain import OrchestratorBrain


class TestOrchestratorBrainInitialization:
    """Test orchestrator brain initialization and core capabilities."""

    @pytest.fixture
    def mock_workspace(self):
        """Create a temporary workspace for testing."""
        workspace = Path(__file__).parent.parent / "workspace"
        return workspace

    @pytest.fixture
    def orchestrator(self, mock_workspace):
        """Create orchestrator instance."""
        brain = OrchestratorBrain(str(mock_workspace))
        return brain

    async def test_initialize_success(self, orchestrator):
        """Test successful initialization."""
        result = await orchestrator.initialize()

        assert result["success"] is True
        assert orchestrator.task_active is False
        assert orchestrator.status_state == "idle"

    async def test_initialize_already_initialized(self, orchestrator):
        """Test re-initialization after already initialized."""
        await orchestrator.initialize()
        result = await orchestrator.initialize()

        assert result["success"] is True

    async def test_get_status_initial(self, orchestrator):
        """Test initial status retrieval."""
        status = await orchestrator.get_status()

        assert "state" in status
        assert "task_active" in status
        assert "tools_count" in status
        assert "modules_count" in status
        assert status["task_active"] is False


class TestToolRegistrySystem:
    """Test tool registry system capabilities."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_register_tool_success(self, orchestrator):
        """Test successful tool registration."""
        result = await orchestrator.register_tool(
            name="test_tool",
            description="A test tool for validation",
            code="def execute(args):\n    return {'result': 'success'}",
            category="backend",
        )

        assert result["success"] is True
        assert "message" in result

    async def test_register_duplicate_tool(self, orchestrator):
        """Test registering duplicate tool."""
        await orchestrator.register_tool(
            name="test_tool",
            description="First registration",
            code="def execute(args):\n    return {'result': 'success'}",
            category="backend",
        )

        result = await orchestrator.register_tool(
            name="test_tool",
            description="Duplicate registration",
            code="def execute(args):\n    return {'error': 'duplicate'}",
            category="backend",
        )

        assert result["success"] is False
        assert "already registered" in result.get("error", "").lower()

    async def test_list_tools(self, orchestrator):
        """Test listing all tools."""
        await orchestrator.register_tool(
            name="tool1",
            description="First tool",
            code="def execute(args):\n    return {}",
        )

        await orchestrator.register_tool(
            name="tool2",
            description="Second tool",
            code="def execute(args):\n    return {}",
        )

        tools = await orchestrator.list_tools()

        assert len(tools) == 2
        assert all("name" in t for t in tools)
        assert all("description" in t for t in tools)

    async def test_list_tools_by_category(self, orchestrator):
        """Test listing tools filtered by category."""
        await orchestrator.register_tool(
            name="backend_tool",
            description="Backend tool",
            code="def execute(args):\n    return {}",
            category="backend",
        )

        await orchestrator.register_tool(
            name="ui_tool",
            description="UI tool",
            code="def execute(args):\n    return {}",
            category="ui",
        )

        backend_tools = await orchestrator.list_tools(category="backend")
        ui_tools = await orchestrator.list_tools(category="ui")

        assert len(backend_tools) == 1
        assert len(ui_tools) == 1

    async def test_hot_load_tool(self, orchestrator):
        """Test hot-loading a tool."""
        # First register the tool
        await orchestrator.register_tool(
            name="hotload_test",
            description="Tool for hot-load testing",
            code="def execute(args):\n    return {'status': 'loaded'}",
        )

        result = await orchestrator.hot_load_tool("hotload_test")

        assert result["success"] is True

    async def test_remove_tool(self, orchestrator):
        """Test removing a tool."""
        await orchestrator.register_tool(
            name="remove_test",
            description="Tool for remove testing",
            code="def execute(args):\n    return {}",
        )

        result = await orchestrator.remove_tool("remove_test")

        assert result["success"] is True

        # Verify tool is removed
        tools = await orchestrator.list_tools()
        assert not any(t["name"] == "remove_test" for t in tools)


class TestAutoAdaptationEngine:
    """Test auto-adaptation engine capabilities."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_get_all_modules(self, orchestrator):
        """Test getting all loaded modules."""
        modules = orchestrator.auto_adaptation.get_all_modules()

        assert isinstance(modules, dict)
        assert "backend" in modules or len(modules) > 0

    async def test_test_module_success(self, orchestrator):
        """Test successful module testing."""
        result = await orchestrator.auto_adaptation.test_module("base_tools", "backend")

        assert result["success"] is True

    async def test_run_self_improvement_loop(self, orchestrator):
        """Test running self-improvement loop."""
        result = await orchestrator.run_self_improvement_loop()

        assert "errors_fixed" in result
        assert "total_errors" in result


class TestFileOperations:
    """Test file operation capabilities (read, write, create, edit)."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_read_file(self, orchestrator):
        """Test reading a file."""
        result = await orchestrator.file_operations.read_file("README.md")

        assert result["success"] is True
        content = result.get("data", "")
        assert isinstance(content, str)
        assert len(content) > 0

    async def test_write_file(self, orchestrator):
        """Test writing to a file."""
        result = await orchestrator.file_operations.write_file(
            "test_output.txt", "Hello, World!"
        )

        assert result["success"] is True

    async def test_create_folder(self, orchestrator):
        """Test creating a folder."""
        result = await orchestrator.file_operations.create_folder("test_folder")

        assert result["success"] is True

    async def test_edit_file(self, orchestrator):
        """Test editing a file (search/replace)."""
        # First create a file with content to edit
        await orchestrator.file_operations.write_file(
            "edit_test.txt", "This is the original content"
        )

        result = await orchestrator.file_operations.edit_file(
            "edit_test.txt",
            edits=[{"op": "replace", "path": "original", "value": "modified"}],
        )

        assert result["success"] is True

        # Verify edit worked
        content = await orchestrator.file_operations.read_file("edit_test.txt")
        assert "modified" in content


class TestAgentInstructionsLoading:
    """Test agent instructions loading system."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_load_instructions_from_list(self, orchestrator):
        """Test loading instructions from a list."""
        instructions = [
            {"description": "Always validate inputs", "priority": "high"},
            {"description": "Use available tools efficiently", "priority": "medium"},
        ]

        result = await orchestrator.load_agent_instructions(instructions)

        assert result["success"] is True
        assert len(orchestrator.agent_instructions) == 2

    async def test_load_instructions_from_file(self, orchestrator):
        """Test loading instructions from a file."""
        # Create a temporary instructions file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                [{"description": "From file instruction 1", "priority": "high"}], f
            )
            temp_path = f.name

        try:
            result = await orchestrator.load_instructions_from_file(temp_path)

            assert result["success"] is True
            assert len(orchestrator.agent_instructions) == 1
        finally:
            import os

            os.unlink(temp_path)


class TestFrontendConnection:
    """Test frontend WebSocket connection capabilities."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_emit_status(self, orchestrator):
        """Test emitting status updates."""
        await orchestrator._emit_status(
            "connected", {"tools_count": 5, "agent_instructions_count": 2}
        )

        # Status should be emitted (no exception)

    async def test_emit_thought(self, orchestrator):
        """Test emitting thoughts."""
        await orchestrator._emit_thought("Thinking about how to solve this problem...")

        # Thought should be emitted (no exception)

    async def test_emit_action(self, orchestrator):
        """Test emitting action results."""
        success_action = {"success": True, "output": "Action completed successfully"}

        await orchestrator._emit_action(success_action)

        error_action = {"success": False, "error": "Something went wrong"}

        await orchestrator._emit_action(error_action)


class TestOrchestrationLoop:
    """Test orchestration loop capabilities."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_start_mission(self, orchestrator):
        """Test starting a mission."""
        result = await orchestrator.start_mission("Test mission")

        assert result["success"] is True
        assert orchestrator.task_active is True

    async def test_stop_mission(self, orchestrator):
        """Test stopping a mission."""
        # Start a mission first
        await orchestrator.start_mission("Test mission")

        # Stop the mission
        orchestrator.stop_task()

        assert orchestrator.task_active is False


class TestSelfImprovementLoop:
    """Test self-improvement loop capabilities (admin mode)."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_run_self_improvement_loop(self, orchestrator):
        """Test running self-improvement loop for admin mode."""
        result = await orchestrator.run_self_improvement_loop()

        assert "errors_fixed" in result
        assert "total_errors" in result


class TestToolCreationAndAddition:
    """Test tool creation and addition capabilities (brain evolution)."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_create_new_tool(self, orchestrator):
        """Test creating a new tool and adding to registry."""
        result = await orchestrator.register_tool(
            name="evolution_test",
            description="A newly evolved tool",
            code="""
def execute(args):
    return {
        'status': 'success',
        'data': args.get('data', {})
    }
""",
            category="backend",
        )

        assert result["success"] is True

    async def test_add_tool_with_schema(self, orchestrator):
        """Test adding a tool with schema definition."""
        schema = {
            "name": "schema_test",
            "description": "Tool with schema",
            "parameters": [{"name": "data", "type": "object"}],
        }

        result = await orchestrator.register_tool(
            name="schema_test",
            description="Tool with schema",
            code="def execute(args):\n    return args",
            schema=schema,
            category="api",
        )

        assert result["success"] is True


class TestMissionReviewValidation:
    """Comprehensive mission review tests for all capabilities."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_loading_agent_instructions_for_flow(self, orchestrator):
        """Test that agent instructions are properly loaded for the flow."""
        instructions = [
            {
                "description": "Always validate inputs before processing",
                "priority": "high",
            },
            {"description": "Use available tools efficiently", "priority": "medium"},
            {
                "description": "Handle errors gracefully with retries",
                "priority": "high",
            },
        ]

        result = await orchestrator.load_agent_instructions(instructions)

        assert result["success"] is True
        assert len(orchestrator.agent_instructions) == 3

        # Verify instructions are in system prompt
        status = await orchestrator.get_status()
        assert "agent_instructions_count" in status

    async def test_core_logic_works_in_loop(self, orchestrator):
        """Test that core logic works properly in a loop."""
        # Test file operations work correctly
        result = await orchestrator.file_operations.write_file(
            "loop_test.txt", "Loop test content"
        )

        assert result["success"] is True

        # Verify we can read it back
        read_result = await orchestrator.file_operations.read_file("loop_test.txt")
        assert read_result["success"] is True
        assert "Loop test content" in read_result.get("data", "")

    async def test_proper_tool_to_write_files(self, orchestrator):
        """Test tool capability to write files."""
        result = await orchestrator.file_operations.write_file(
            "test_mission_review.txt", "Mission review test content"
        )

        assert result["success"] is True

    async def test_proper_tool_to_edit_files(self, orchestrator):
        """Test tool capability to edit files."""
        # Create file first
        await orchestrator.file_operations.write_file(
            "edit_test.txt", "Original content"
        )

        result = await orchestrator.file_operations.edit_file(
            "edit_test.txt", search="Original", replace="Modified"
        )

        assert result["success"] is True

    async def test_proper_tool_to_read_files(self, orchestrator):
        """Test tool capability to read files."""
        await orchestrator.file_operations.write_file(
            "read_test.txt", "Content to read"
        )

        result = await orchestrator.file_operations.read_file("read_test.txt")

        assert isinstance(result, str)
        assert "Content to read" in result

    async def test_proper_tool_to_create_folders(self, orchestrator):
        """Test tool capability to create folders."""
        result = await orchestrator.file_operations.create_folder(
            "test_mission_review_folder"
        )

        assert result["success"] is True

    async def test_connect_frontend_capability(self, orchestrator):
        """Test frontend connection capability (status emission)."""
        # Test emitting various status types
        await orchestrator._emit_status("connected", {"tools_count": 0})
        await orchestrator._emit_thought("Testing thought emission")
        await orchestrator._emit_action({"success": True, "output": "Test action"})

        # All emissions should complete without error

    async def test_robust_core_logic(self, orchestrator):
        """Test that core logic is robust and handles various scenarios."""
        # Test 1: Multiple tool registrations
        for i in range(3):
            await orchestrator.register_tool(
                name=f"robust_test_{i}",
                description=f"Robust test tool {i}",
                code="def execute(args):\n    return args",
                category="backend",
            )

        # Test 2: Load instructions
        instructions = [
            {"description": "Instruction 1"},
            {"description": "Instruction 2"},
        ]
        await orchestrator.load_agent_instructions(instructions)

        # Test 3: Get status multiple times
        for _ in range(3):
            status = await orchestrator.get_status()
            assert "state" in status

    async def test_autoadapt_hot_loaded_modules_ability(self, orchestrator):
        """Test auto-adaptation with hot-loaded modules ability."""
        # Test getting all modules
        modules = orchestrator.auto_adaptation.get_all_modules()

        # Test testing a module
        result = await orchestrator.auto_adaptation.test_module("base_tools", "backend")

        assert result["success"] is True

    async def test_orchestrator_brain_core_with_tools(self, orchestrator):
        """Test that orchestrator brain core has tools and can add new ones."""
        # Verify initial state
        initial_tools = await orchestrator.list_tools()

        # Add a new tool
        result = await orchestrator.register_tool(
            name="brain_evolution_tool",
            description="A tool added to the brain's evolution",
            code="def execute(args):\n    return {'evolved': True}",
            category="backend",
        )

        assert result["success"] is True

        # Verify tool was added
        final_tools = await orchestrator.list_tools()
        assert any(t["name"] == "brain_evolution_tool" for t in final_tools)


class TestComprehensiveMissionReview:
    """Final comprehensive mission review test."""

    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator instance with mock workspace."""
        workspace = Path(__file__).parent.parent / "workspace"
        brain = OrchestratorBrain(str(workspace))
        await brain.initialize()
        return brain

    async def test_all_capabilities_loaded_properly(self, orchestrator):
        """Test that all capabilities are loaded properly for the flow."""
        # 1. Tool registry system
        tools = await orchestrator.list_tools()
        assert isinstance(tools, list)

        # 2. Auto-adaptation engine
        modules = orchestrator.auto_adaptation.get_all_modules()
        assert isinstance(modules, dict)

        # 3. File operations
        result = await orchestrator.file_operations.write_file(
            "mission_review_final.txt", "All capabilities loaded properly"
        )
        assert result["success"] is True

        # 4. Agent instructions loading
        instructions = [{"description": "Final instruction test"}]
        await orchestrator.load_agent_instructions(instructions)
        assert len(orchestrator.agent_instructions) == 1

        # 5. Frontend connection (status emission)
        await orchestrator._emit_status(
            "complete", {"message": "All capabilities loaded properly"}
        )

        # 6. Robust core logic
        status = await orchestrator.get_status()
        assert all(key in status for key in ["state", "task_active", "tools_count"])

        # 7. Auto-adaptation with hot-loading
        result = await orchestrator.auto_adaptation.test_module("base_tools", "backend")
        assert result["success"] is True

        return {
            "tool_registry": True,
            "auto_adaptation": True,
            "file_operations": True,
            "agent_instructions": True,
            "frontend_connection": True,
            "robust_core_logic": True,
            "hot_loading": True,
        }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
