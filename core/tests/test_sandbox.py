import pytest
from modules.sandbox import WorkspaceGuard


@pytest.fixture
def sandbox(tmp_path):
    """Provides a WorkspaceGuard jailed to a temporary directory."""
    return WorkspaceGuard(str(tmp_path.absolute()))


def test_sandbox_resolve_safe(sandbox):
    """READ should be safe within the root."""
    path = sandbox.secure_path("test.txt", write=False)
    assert sandbox.root in path.parents
    assert path.name == "test.txt"


def test_sandbox_write_safe(sandbox):
    """WRITE should be safe within the root."""
    path = sandbox.secure_path("subfolder/test.py", write=True)
    assert sandbox.root in path.parents
    assert "subfolder" in str(path)


def test_sandbox_traversal_attack(sandbox):
    """Verify that traversal above root is blocked."""
    with pytest.raises(PermissionError, match="Security Alert: Path traversal detected"):
        sandbox.secure_path("../secret.txt")


def test_sandbox_absolute_path_attack(sandbox):
    """Verify that absolute paths outside root are blocked."""
    # This might behave differently depending on how pathlib handles it,
    # but WorkspaceGuard should block it.
    with pytest.raises(PermissionError):
        sandbox.secure_path("/etc/passwd")


def test_delete_routing_to_trash(sandbox):
    """Verify that delete moves files to the .trash folder within root."""
    # Setup a file
    test_file = sandbox.root / "to_delete.txt"
    test_file.touch()

    # Delete it
    sandbox.safe_delete("to_delete.txt")

    trash_path = sandbox.root / ".trash" / "to_delete.txt"
    assert not test_file.exists()
    assert trash_path.exists()


def test_sandbox_core_isolation(sandbox):
    """Verify that writing outside the root (e.g. to core/) is blocked."""
    # In WorkspaceGuard, any path passed is relative to root.
    # So if we try to 'escape' via ../core/main.py, it should fail.
    with pytest.raises(PermissionError, match="Security Alert"):
        sandbox.secure_path("../core/main.py", write=True)
