import os
from pathlib import Path
from typing import Union


class WorkspaceGuard:
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root).resolve()
        self.trash = self.root / ".trash"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.trash.mkdir(parents=True, exist_ok=True)

    def secure_path(self, relative_path: Union[str, Path]) -> Path:
        """
        Resolves a path relative to workspace root and ensures it's within bounds.
        Throws PermissionError if path escapes root or attempts to modify core/ (immutable).
        """
        requested_path = (self.root / relative_path).resolve()

        # Security check 1: Path traversal detection
        if not str(requested_path).startswith(str(self.root)):
            raise PermissionError(
                f"Security Alert: Path traversal detected! {relative_path} escapes root."
            )

        # Security check 2: Core directory is immutable (coupled with other models)
        core_path = self.root / "core"
        if str(requested_path).startswith(str(core_path)):
            raise PermissionError(
                f"Security Alert: Core directory is IMMUTABLE! Cannot modify {relative_path}. "
                f"Core/ is coupled with other models and must remain unchanged."
            )

        return requested_path

    def safe_delete(self, relative_path: str):
        """
        Moves a file to the .trash folder instead of deleting it.
        """
        target = self.secure_path(relative_path)
        if not target.exists():
            return

        trash_path = self.trash / target.name
        # Handle naming collisions in trash
        counter = 1
        while trash_path.exists():
            trash_path = self.trash / f"{target.stem}_{counter}{target.suffix}"
            counter += 1

        os.rename(target, trash_path)

    def is_safe(self, path: str) -> bool:
        try:
            self.secure_path(path)
            return True
        except PermissionError:
            return False
