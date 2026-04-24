import pytest
from unittest.mock import MagicMock, patch
from modules.coder import SmolAgentWrapper

@pytest.fixture
def mock_base_tools():
    tools = MagicMock()
    return tools

def test_smol_agent_initialization(mock_base_tools):
    # Patch LiteLLMModel to avoid actual API calls
    with patch("modules.coder.LiteLLMModel"):
        wrapper = SmolAgentWrapper(mock_base_tools, "/fake/workspace")
        assert wrapper.base_tools == mock_base_tools
        assert wrapper.workspace_root == "/fake/workspace"
        assert len(wrapper.agent.tools) >= 4

@pytest.mark.asyncio
async def test_run_task_success(mock_base_tools):
    with patch("modules.coder.LiteLLMModel"):
        wrapper = SmolAgentWrapper(mock_base_tools, "/fake/workspace")

        # Mock the synchronous agent run method
        wrapper.agent.run = MagicMock(return_value="Task complete")

        result = await wrapper.run_task("Fix bug", "app.py", "pytest")

        assert result["success"] is True
        assert result["result"] == "Task complete"
        wrapper.agent.run.assert_called_once()

@pytest.mark.asyncio
async def test_run_task_failure(mock_base_tools):
    with patch("modules.coder.LiteLLMModel"):
        wrapper = SmolAgentWrapper(mock_base_tools, "/fake/workspace")

        # Mock to throw exception
        wrapper.agent.run = MagicMock(side_effect=Exception("API Error"))

        result = await wrapper.run_task("Fix bug", "app.py", "pytest")

        assert result["success"] is False
        assert "API Error" in result["error"]
