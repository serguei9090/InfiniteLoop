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
    # READ should be safe anywhere
    path = sandbox.secure_path("test.txt", write=False)
    assert "test_workspace" in str(path)
    assert path.name == "test.txt"


def test_sandbox_resolve_apps_write(sandbox):
    # WRITE should be safe in Apps
    path = sandbox.secure_path("Apps/test.txt", write=True)
    assert "Apps" in str(path)


def test_sandbox_traversal_attack(sandbox):
    with pytest.raises(PermissionError):
        sandbox.secure_path("../secret.txt")


def test_sandbox_absolute_path_attack(sandbox):
    # Depending on OS, this might vary, but should always fail
    with pytest.raises(PermissionError):
        sandbox.secure_path("/etc/passwd")


def test_delete_routing_to_trash(sandbox):
    # Setup a file in Apps
    apps_file = sandbox.apps / "test_delete.txt"
    apps_file.touch()
    
    # Delete it
    sandbox.safe_delete("Apps/test_delete.txt")

    trash_path = sandbox.trash / "test_delete.txt"
    assert not apps_file.exists()
    assert trash_path.exists()


def test_sandbox_apps_isolation(sandbox):
    # Should be able to resolve/write inside Apps
    apps_path = sandbox.secure_path("Apps/my_app.py", write=True)
    assert "Apps" in str(apps_path)

    # Should NOT be able to write outside Apps
    with pytest.raises(PermissionError) as excinfo:
        sandbox.secure_path("core/main.py", write=True)
    assert "WRITE BLOCKED" in str(excinfo.value)
