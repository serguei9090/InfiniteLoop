# Technical Specification: Core Intelligence Refactor & Sandbox Hardening (OP_CLEAN_BRAIN_V1)

## Executive Summary
This specification outlines the refactoring of the IMMUTABLE CORE backend. The goal is to enforce architectural purity by separating concerns between the orchestrator's brain and its thinking process, while simultaneously hardening the execution sandbox to prevent any accidental or malicious file deletions.

## Requirements

### R1: Thinking Module Extraction
- **Goal**: Move token-level stream parsing and thinking state out of the main orchestrator.
- **Location**: `core/modules/thinking.py`
- **Functional Requirements**:
  - Intercept and parse `<|think|>` and `<|/think|>` tags.
  - Expose a clean interface for the `OrchestratorBrain` to stream just the "monologue" to the UI.
  - Maintain the circuit breaker logic (max retries).

### R2: Sandbox Hardening
- **Goal**: Ensure the AI cannot permanently delete files.
- **Rules**:
  - All "deletes" must be intercepted and routed to `workspace/.trash/`.
  - The `WorkspaceGuard` must be updated to explicitly forbid `remove` or `rmdir` calls on any file outside the `.trash` zone.
  - Implement a `SafeFileIO` context manager or decorator to enforce these rules globally within the tool engine.

### R3: Context Engine Expansion
- **Goal**: Improve the agent's architectural awareness beyond Python/TS.
- **Extension**: Add Tree-sitter parsers for:
  - **CSS**: Extract selectors and styles.
  - **HTML**: Extract major tags and IDs.
  - **Markdown**: Extract headers and structure.

## Tech Stack
- **Backend**: Python 3.12 (managed via `uv`).
- **Parsing**: Tree-sitter.
- **State**: Persistent via `orchestrator_brain.py`.

## Data Flow
1. **LLM Output (Stream)** -> `ThinkingModule` -> **(Monologue) UI**
2. **LLM Output (JSON)** -> `ToolEngine` -> `SandboxGuard` -> **Filesystem (workspace)**
