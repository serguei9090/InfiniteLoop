# PRD: Operation "Modern Core" (ADK 2.0 Migration)

## 🎯 Vision
Transform InfiniteLoop into a state-of-the-art agentic factory by replacing custom orchestration with the **Google ADK SDK**, enforcing absolute modular purity, and eliminating legacy technical debt.

## 📐 Success Metrics (Definition of Done)
1. **ADK Purity**: `OrchestratorBrain` successfully uses `google.adk.Agent` and `LoopRunner`.
2. **Zero Legacy**: `cli/main.py` and `cli/infinite.py` consolidated into a unified `infinite` command.
3. **Tool Compliance**: All `BaseTools` use ADK docstring schemas; no manual JSON schema overrides.
4. **Environment Stability**: `uv run infinite` starts the ADK-powered loop without errors.

## 📋 Surgical Task List

### 1. The Purity Pass (Cleanup)
- [ ] Delete `cli/main.py`.
- [ ] Consolidation check on `cli/infinite.py` and `cli/pyproject.toml`.
- [ ] Rename/Organize `core/main.py` into `core/api/routes.py` (if applicable).

### 2. Tool Evolution (Backend)
- [ ] Refactor `core/modules/base_tools.py` for ADK docstring compliance.
- [ ] Implement `core/modules/adk_tools.py` to bridge existing logic to the new `Agent` model.

### 3. The Brain Transplant (Architect)
- [ ] Create `core/modules/adk_agent.py` using `google.adk.Agent`.
- [ ] Update `cli/infinite.py` to spawn the `ADKAgent` instead of `OrchestratorBrain`.
- [ ] Archive `core/modules/orchestrator_brain.py` and `core/modules/thinking.py` once validated.

### 4. Integration & UI
- [ ] Ensure the UI `/dashboard` receives ADK events via the `StreamHandler`.
- [ ] Verify `adk web` capability for remote debugging.

---

## 🛡️ Risk Assessment
- **Breaking Bridge**: Switching from custom stream parsing to ADK's `Runner` might affect UI updates.
- **Model Compatibility**: ensuring LM Studio/LiteLLM works flawlessly with `Agent(model=...)`.
