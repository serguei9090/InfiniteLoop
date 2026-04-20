# TODO(sandbox_refactor_001): Designated Writable Territory (Apps/)

## Description
Refactor `WorkspaceGuard` to restrict WRITE operations exclusively to the `Apps/` and `.trash/` directories. All other project directories (including `core/`) will be READ-ONLY for the agent.

## Why
1. To prevent accidental corruption of the "Immutable Core".
2. To provide a safe, designated workspace (`Apps/`) for the agent to build and evolve applications.
3. To resolve the "immutable core" bottleneck reported in logs by funneling creative output into a specific folder.

## Implementation Plan

### 1. File Structure
- [ ] Create `i:\01-Master_Code\Test-Labs\InfiniteLoop\Apps`.
- [ ] Ensure `.gitignore` ignores non-essential `Apps/` content if necessary.

### 2. Sandbox Engine Update (`core/modules/sandbox.py`)
- [ ] Update `WorkspaceGuard.__init__` to track `self.apps`.
- [ ] Refactor `secure_path` to:
    - [ ] Allow READ operations anywhere in the root.
    - [ ] Allow WRITE operations ONLY in `Apps/` or `.trash/`.
    - [ ] Provide descriptive error messages for blocked writes.

### 3. Toolset Verification (`core/modules/base_tools.py`)
- [ ] Verify that `write_file`, `create_folder`, and `delete_file` behave correctly with the new rules.

### 4. Integration Test
- [ ] Add a test case in `core/tests/test_sandbox.py` (or similar) to verify:
    - [ ] `Apps/file.txt` is writable.
    - [ ] `core/main.py` is NOT writable.
    - [ ] Recursive creation in `Apps/` works.

## Acceptance Criteria
- [ ] Agent can read any file in the workspace.
- [ ] Agent CANNOT write to any file outside `Apps/` or `.trash/`.
- [ ] Attempting to write outside `Apps/` returns a clear "Read-Only Territory" error.
