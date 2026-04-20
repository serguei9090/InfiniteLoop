import pytest
from pathlib import Path
from modules.sandbox import WorkspaceGuard


@pytest.fixture
def sandbox():
    # Use a test workspace relative to current
    test_path = Path("test_workspace")
    test_path.mkdir(exist_ok=True)
    return WorkspaceGuard(str(test_path.absolute()))


def test_sandbox_resolve_safe(sandbox):
    path = sandbox.secure_path("test.txt")
    assert "test_workspace" in str(path)
    assert path.name == "test.txt"


def test_sandbox_traversal_attack(sandbox):
    with pytest.raises(PermissionError):
        sandbox.secure_path("../secret.txt")


def test_sandbox_absolute_path_attack(sandbox):
    # Depending on OS, this might vary, but should always fail
    with pytest.raises(PermissionError):
        sandbox.secure_path("/etc/passwd")


def test_delete_routing_to_trash(sandbox):
    test_file = sandbox.root / "test_delete.txt"
    test_file.touch()
    sandbox.safe_delete("test_delete.txt")

    trash_path = sandbox.trash / "test_delete.txt"
    assert not test_file.exists()
    assert trash_path.exists()
