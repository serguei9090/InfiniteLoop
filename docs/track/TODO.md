# TODO: Project Intelligence Refactor (OP_CLEAN_BRAIN_V1)

## Phase 1: Thinking Logic Extraction
- [x] Create `core/modules/thinking.py` with `ThinkingEngine` class. [ID: core_refactor_001]
- [x] Migrate stream parsing logic from `orchestrator_brain.py` to `ThinkingEngine`.
- [x] Update `OrchestratorBrain` to use `ThinkingEngine` for all stream intercepts.
- [x] Verify thought stream is still correctly emitted to frontend.

## Phase 2: Sandbox Hardening [DONE]
- [x] Audit `core/modules/sandbox.py` for direct `os` removal methods. [ID: sandbox_hardening_001]
- [x] Implement `TrashRedirector` in `base_tools.py`.
- [x] Add unit test verifying that `delete_file` tool moves to `.trash` instead of deleting.
- [x] Implement `Apps/` Isolation (Only writable territory outside .trash). [ID: sandbox_refactor_001]

## Phase 3: Context Engine Expansion
- [x] Add Tree-sitter parsers for CSS/HTML/Markdown in `core/modules/context.py`. [ID: context_expansion_001]
- [x] Update `BaseTools.read_file` to support new skeleton types.
- [x] Verify contextual awareness with a complex UI codebase.

## Phase 4: Final Validation
- [ ] Run full test suite.
- [ ] Verify "Observer UI" correctly displays monologue during complex tasks.
