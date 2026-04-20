---
description: Jules CLI Standards and Usage Guidelines
---

# Jules CLI Documentation & Rules

Jules is a remote asynchronous coding agent. Use the CLI to delegate long-running tasks or multi-file refactors.

## 1. Commands Overview

| Command | Use Case |
| :--- | :--- |
| `jules remote new` | Starts a new remote coding session. Defaults to the current repo. |
| `jules remote list --session` | Lists all active and past sessions with their completion status. |
| `jules remote pull` | Retrieves the results of a completed session as a diff. |
| `jules remote teleport` | Clones the repo to a temp dir and applies the session patch (Best for clean tests). |

## 2. Standard Workflow Rules

### A. Initialization & Handoff
- **Commit & Push**: Before starting a new session, you **MUST** ensure all local changes are committed and pushed upstream to GitHub so the remote agent has the latest code.
- **Handoff Manifest**: Before starting a new session, you **MUST** generate a `handoff.json` in the `temp/` folder (as defined in `agents.yaml`).
- **Manifest Content**: Include the *Active Task ID, Current Context, Constraints, and Rejected Paths*.
- **Prompt Injection**: Always include a reference to the handoff manifest in the `--session` prompt: *"Refer to handoff.json for the latest architectural state and task boundaries."*
- **Local Context**: Ensure the repository is specified using `--repo .` and the session is recorded using `--record`.

### B. Monitoring
- Use `jules remote list --session` periodically.
- Check the **Status** column:
  - `In Progress`: Agent is still thinking/coding.
  - `Completed`: Patch is ready to pull.
  - `Failed`: Something went wrong in the cloud environment.
  - `Awaiting User Feedback`: Jules needs clarification.

### C. Integration & Sync
1. **Dry-Run**: Always run `jules remote pull --session <ID>` first to inspect the diff.
2. **Apply & Update Manifest**: Use `jules remote pull --session <ID> --apply`. Once merged, update the `handoff.json` to reflect the new project state.
3. **Conflict Resolution**: If the patch fails to apply (due to local edits):
   - Commit your local work first.
   - Use `jules remote teleport <ID>` to see the "golden version" of the fix.
   - Manually merge if necessary.

## 3. High-Efficiency Jules Rules (Anti-Scripting)

### A. Task Precision
To prevent Jules from generating fragile helper scripts (e.g., Python regex mutators) that fail in CI:
- **Rule**: Explicitly instruct Jules in the prompt: *"Perform direct file modifications using [Language] syntax. Do not generate intermediate helper scripts for patching."*
- **Scope**: Keep tasks atomic. Focus on one module or one specific performance optimization per session.

### B. Handling "Awaiting Feedback"
If a session status shows `Awaiting User Feedback`:
- **Action**: Use the `jules remote pull --session <ID>` command. It will often output the question or ambiguity Jules hit.
- **Resolution**: If the CLI doesn't show the question, visit the URL provided in the session list to answer Jules.

### C. Post-Pull Validation
After a successful `--apply`:
- Always run `npm run check`, `uv run ruff`, or equivalent project-specific verification immediately.

## 4. Tracking Protocol (Mandatory)
Every time a new session is launched, pulled, or fails, you **MUST** update `docs/track/JULES.md`.
- **Purpose**: Prevents duplicate pulls, tracks failed automation attempts, and maintains historical context.
- **Fields**: Session ID, Task Description, internal Jules Status, and whether it has been Merged Locally.

## 5. Command Examples

```powershell
# Create a session for code optimization
jules remote new --repo . --session "Optimize data processing loops in core modules. Perform direct file modifications. Do not use intermediate scripts." --record

# Check if it is done
jules remote list --session

# Pull and apply
jules remote pull --session <ID> --apply
```
