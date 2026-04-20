# Objective
Implement a clear separation of concerns in the ADK agent so it can seamlessly switch between self-evolution and application building based on CLI flags.

# Key Files & Context
- `core/modules/adk_agent.py`: Houses the `ADKOrchestrator` and its system prompt.
- `cli/infinite.py`: The CLI entry point that triggers the orchestrator.

# Implementation Steps

1. **Update `core/modules/adk_agent.py` (ADK Orchestrator)**:
    - **Constructor Update**: Modify `__init__` to accept a `target_workspace` argument (e.g., `"workspace"` or `"UserWorkspace/main_app"`). Update `self.workspace_root` to resolve against this target path.
    - **Engine Initialization**: Ensure `WorkspaceGuard`, `EvolutionEngine`, and `AutoAdaptationEngine` are initialized with the dynamic `self.workspace_root`.
    - **Prompt Injection**: Update `_get_base_instructions()` to dynamically format the sandbox boundaries in the prompt (replacing the hardcoded `workspace/` string with the `target_workspace` path) so the AI correctly understands its boundaries.

2. **Update `cli/infinite.py` (CLI Interface)**:
    - **Command Renaming**: Rename the `autoevolve` command to `evolve` for a unified entry point.
    - **Flag Addition**: Introduce a `--self` flag (boolean) and an `--app` flag (string, defaulting to `"main_app"`).
    - **Routing Logic**: Update the initialization so that if `--self` is active, the `ADKOrchestrator` is initialized with `target_workspace="workspace"`. Otherwise, it is initialized with `target_workspace=f"UserWorkspace/{app}"`.

# Verification & Testing
- Run `uv run python cli/infinite.py evolve --self --mission "List tools"` and verify the agent accesses `workspace/`.
- Run `uv run python cli/infinite.py evolve --app test_app --mission "Create README"` and verify the agent is jailed exclusively to `UserWorkspace/test_app/` and correctly outputs its tasks there.
