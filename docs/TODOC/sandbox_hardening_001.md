# TODO(sandbox_hardening_001): Sandbox & Trash Hardening

## Description
Enforce the "No RM" rule by ensuring all deletions are routed to the `.trash` folder.

## Why
Security and safety. We don't want the AI to accidentally delete project source or logs during a self-evolution fail.

## Implementation Strategy
1. **Sandbox Update**: In `core/modules/sandbox.py`, add a check in `is_safe_path` or a new `validate_operation` method that rejects `os.remove` if the path isn't in `.trash`.
2. **Tool Update**: Ensure `base_tools.py` uses `shutil.move` instead of `os.remove`.
3. **Guardrails**: Implement a "Strict Mode" that can be toggled via config.

## Acceptance Criteria
- [ ] No direct `os.remove` calls in toolchain.
- [ ] Attempting to delete a file results in its appearance in `workspace/.trash/`.
