import pytest
import shutil
from pathlib import Path
from modules.sandbox import WorkspaceGuard
from modules.context import ContextEngine


@pytest.fixture(scope="module")
def sandbox():
    test_path = Path("test_workspace_validation")
    test_path.mkdir(exist_ok=True)
    yield WorkspaceGuard(str(test_path.absolute()))
    shutil.rmtree(test_path, ignore_errors=True)


def test_sandbox_path_traversal_prevention(sandbox):
    with pytest.raises(
        PermissionError, match="Security Alert: Path traversal detected"
    ):
        sandbox.secure_path("../../../etc/passwd")


def test_sandbox_absolute_path_prevention(sandbox):
    with pytest.raises(
        PermissionError, match="Security Alert: Path .* is outside root"
    ):
        sandbox.secure_path("/etc/passwd")


def test_context_compression_accuracy(sandbox):
    # Setup test python file
    test_file = sandbox.root / "compression_test.py"
    with open(test_file, "w") as f:
        f.write(
            '"""Module docstring"""\ndef test():\n    # Test comment\n    print("Hello")'
        )

    engine = ContextEngine()
    compressed = engine.get_full_compressed(test_file)

    assert "Module docstring" not in compressed
    assert "Test comment" not in compressed
    assert 'print("Hello")' in compressed


def test_tech_stack_adherence():
    ui_package = Path("../ui/package.json")
    if ui_package.exists():
        content = ui_package.read_text()
        assert "react" in content.lower()
