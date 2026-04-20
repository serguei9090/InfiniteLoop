---
name: session-handover
description: Specialized skill for ensuring context continuity between AI sessions. Use this to perform a "Session Wrap-up" that generates a handoff file for the next session's AI assistant.
---

# Session Handover Skill

This skill ensures 100% continuity by capturing the exact execution state, blockers, and next steps before a session ends.

## 1. Wrap-up Workflow

When the user requests a "Session Wrap-up" or "Handover," perform these steps:

1.  **Analyze Current State & Telemetry**: Review the internal task list, recent chat history, and `telemetry.csv` to determine the current session length.
2.  **Hard Context Sync Check**: If the session has reached the 50-turn threshold (see `ContextManagement.md`), perform a **Hard Sync**:
    -   Create a comprehensive `docs/archive/sessions/session_[ID]_summary.md`.
    -   Consolidate all `docs/TODOC/` files for that session.
3.  **Verify Parity**: Ensure `docs/track/TODO.md` is updated with all completed tasks (`[x]`).
4.  **Generate Handoff**: Create or update `docs/track/handoff.md` with the following structure:

```markdown
# Session Handoff: [Date/Time]

## 1. Last Action
- [Exactly what was just finished or the last file modified]

## 2. Current Blockers
- [Why we stopped, failing tests, or missing information]

## 3. Contextual Memory
- [Specific technical decisions or chosen libraries made in this session]

## 4. Next Atomic Step
- [The very first small, actionable task for the next session]
```

4.  **Final Summary**: Provide the user with a concise summary of the handoff and confirm that the project state is "Saved and Ready."

## 2. Best Practices

- **Be Atomic**: The "Next Atomic Step" should be small enough to execute in the first 5 minutes of the next session.
- **Traceability**: Reference specific `TODO(ID)` identifiers from `docs/track/TODO.md`.
- **Logic Snippets**: If a complex logic path was discovered but not yet implemented, include it in the "Contextual Memory" or a dedicated `docs/TODOC/` file.
