import os
from pathlib import Path
from typing import Union


class WorkspaceGuard:
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root).resolve()
        self.trash = self.root / ".trash"
        self.apps = self.root / "Apps"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.trash.mkdir(parents=True, exist_ok=True)
        self.apps.mkdir(parents=True, exist_ok=True)

    def secure_path(self, relative_path: Union[str, Path], write: bool = True) -> Path:
        """
        Resolves a path relative to workspace root and ensures it's within bounds.
        Throws PermissionError if path escapes root.
        If write=True, enforces that changes must be in Apps/ or .trash/.
        """
        # Handle potential absolute paths coming from the runner
        path_obj = Path(relative_path)
        if path_obj.is_absolute():
            try:
                relative_path = path_obj.relative_to(self.root)
            except ValueError:
                raise PermissionError(f"Security Alert: Path {relative_path} is outside root {self.root}")

        requested_path = (self.root / relative_path).resolve()

        # Security check 1: Path traversal detection
        if not str(requested_path).startswith(str(self.root)):
            raise PermissionError(
                f"Security Alert: Path traversal detected! {relative_path} escapes root."
            )

        # Security check 2: Write Isolation Principle
        if write:
            # Allow writes ONLY to Apps/ or .trash/
            is_in_apps = str(requested_path).startswith(str(self.apps))
            is_in_trash = str(requested_path).startswith(str(self.trash))

            if not (is_in_apps or is_in_trash):
                raise PermissionError(
                    f"Security Alert: WRITE BLOCKED. The root project is READ-ONLY. "
                    f"You must perform all implementations inside the 'Apps/' directory. "
                    f"Rejected path: {relative_path}"
                )

        return requested_path

    def safe_delete(self, relative_path: str):
        """
        Moves a file to the .trash folder instead of deleting it.
        """
        target = self.secure_path(relative_path, write=True)
        if not target.exists():
            return

        trash_path = self.trash / target.name
        # Handle naming collisions in trash
        counter = 1
        while trash_path.exists():
            trash_path = self.trash / f"{target.stem}_{counter}{target.suffix}"
            counter += 1

        os.rename(target, trash_path)

    def is_safe(self, path: str, write: bool = True) -> bool:
        try:
            self.secure_path(path, write=write)
            return True
        except PermissionError:
            return False
