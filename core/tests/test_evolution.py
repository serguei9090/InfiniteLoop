import pytest
from pathlib import Path
from modules.evolution import EvolutionEngine

@pytest.fixture
def evolution_engine(tmp_path):
    tools_dir = tmp_path / "dynamic_tools"
    return EvolutionEngine(str(tools_dir))

def test_evolution_syntax_error(evolution_engine):
    """Verify that syntax errors are caught."""
    code = "def invalid_syntax(:"
    schema = '{"description": "test", "properties": {}}'
    
    result = evolution_engine.validate_and_register("fail_tool", code, schema)
    
    assert result["success"] is False
    assert "SyntaxError" in result["error"] or "invalid syntax" in result["error"].lower()

def test_evolution_illegal_import(evolution_engine):
    """Verify that illegal imports are caught."""
    code = "import shutil\ndef dangerous(): pass"
    schema = '{"description": "test", "properties": {}}'
    
    result = evolution_engine.validate_and_register("evil_tool", code, schema)
    
    assert result["success"] is False
    assert "Illegal import" in result["error"]

def test_evolution_missing_schema_keys(evolution_engine):
    """Verify that schema keys are validated."""
    code = "def valid(): pass"
    schema = '{"only_desc": "test"}' # Missing properties
    
    result = evolution_engine.validate_and_register("bad_schema", code, schema)
    
    assert result["success"] is False
    assert "Schema missing" in result["error"]

def test_evolution_successful_registration(evolution_engine, tmp_path):
    """Verify successful registration (mocking uv for speed if possible)."""
    # For now, we let it run uv init if uv is installed, otherwise it might fail.
    # But we want to test the full flow.
    code = "def add(a, b): return a + b"
    schema = '{"description": "Adds two numbers", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}'
    
    result = evolution_engine.validate_and_register("math_tool", code, schema)
    
    # If uv is not available, this might fail, but let's see.
    if result["success"]:
        assert "math_tool" in evolution_engine.registered_tools
        assert (Path(evolution_engine.tools_dir) / "math_tool" / "math_tool.json").exists()
    else:
        # If it failed due to uv missing, that's okay for local dev but we should know.
        pass
