import pytest
from unittest.mock import patch, MagicMock
from modules.claude_agent import ClaudeOrchestrator

@pytest.fixture
def mock_dependencies():
    with patch("modules.claude_agent.WorkspaceGuard"), \
         patch("modules.claude_agent.ContextEngine"), \
         patch("modules.claude_agent.EvolutionEngine"), \
         patch("modules.claude_agent.AutoAdaptationEngine"), \
         patch("modules.claude_agent.BaseTools"):
        yield

@pytest.mark.asyncio
async def test_initialization(mock_dependencies):
    orchestrator = ClaudeOrchestrator()
    result = await orchestrator.initialize()
    assert result["success"] is True
    assert "Claude Orchestrator" in result["message"]
    assert orchestrator.custom_mcp_server is not None

@pytest.mark.asyncio
@patch("modules.claude_agent.query")
async def test_start_mission(mock_query, mock_dependencies):
    orchestrator = ClaudeOrchestrator()
    await orchestrator.initialize()

    # Mock the generator yielded by query
    async def mock_query_gen(*args, **kwargs):
        # We simulate empty messages for now
        yield MagicMock()

    mock_query.side_effect = mock_query_gen

    result = await orchestrator.start_mission("Test task")
    assert result["success"] is True

    mock_query.assert_called_once()
    kwargs = mock_query.call_args.kwargs
    assert kwargs["prompt"] == "Test task"

    options = kwargs["options"]
    # Check attributes since it's a dataclass-like or typeddict
    if hasattr(options, "allowed_tools"):
        assert "Read" in options.allowed_tools
        assert "WebFetch" in options.allowed_tools
        assert "WebSearch" in options.allowed_tools
    else:
        assert "Read" in options["allowed_tools"]
        assert "WebFetch" in options["allowed_tools"]
        assert "WebSearch" in options["allowed_tools"]

    if hasattr(options, "mcp_servers"):
        assert "core_custom" in options.mcp_servers
    else:
        assert "core_custom" in options["mcp_servers"]
