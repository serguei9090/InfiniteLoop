# IMMUTABLE CORE - Roadmap & Tasks

## PHASE 1: Core Loop & API Bridge [DONE]
- [x] Scaffold project structure.
- [x] Set up local LLM connector (LM Studio).
- [x] Implement `<|think|>` stream parser.
- [x] Build base termination/loop logic.

## PHASE 2: The Sandbox & Context Manager [DONE]
- [x] Implement `WorkspaceGuard` (Block path traversals).
- [x] Integrate Tree-sitter for skeleton generation.
- [x] Implement dynamic sliding window (Context compression).

## PHASE 3: Reflexion & Tools [DONE]
- [x] Implement base tools: `read_file`, `write_file`, `cmd_exec`.
- [x] Build error-catcher middleware (Reflexion loop).
- [x] Implement retry logic (Max 3).

## PHASE 4: Auto-Evolution [DONE]
- [x] Create file watcher on `.agents/dynamic_tools/`.
- [x] Implement Automated Validation Criteria.
- [x] Implement hot-reloading of tool schemas.
- [x] Add `create_new_tool` command.

## PHASE 5: Observer UI [DONE]
- [x] Build static HTML dashboard.
- [x] Stream `<|think|>` monologue to UI.
- [x] Display tool logs and core metrics.

## PHASE 6: CopilotKit & UV Isolation [DONE]
- [x] Integrate CopilotKit into React Frontend.
- [x] Implement CopilotRuntime in FastAPI Backend.
- [x] Refactor EvolutionEngine to use `uv` for tool isolation.
- [x] Execute dynamic tools via `uv run` in dedicated environments.

**PROJECT BASELINE COMPLETE.**
Core loop is autonomous, sandboxed, self-evolving, observable, and integrated with CopilotKit.
Modules are managed via `uv` virtual environments.
