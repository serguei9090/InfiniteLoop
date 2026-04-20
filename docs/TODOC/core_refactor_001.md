# TODO(core_refactor_001): Thinking Module Migration

## Description
Extract the complex stream parsing and monologue interception logic from `OrchestratorBrain` into a dedicated `ThinkingEngine`.

## Why
`orchestrator_brain.py` is currently over 500 lines and handles too many responsibilities. The architectural spec explicitly requires `core/modules/thinking.py`.

## Implementation Strategy
1. **New Module**: `core/modules/thinking.py`
2. **Key Class**: `ThinkingEngine`
   - `def process_chunk(self, chunk: str) -> Optional[str]`: Processes a chunk and returns the thought text if in thinking mode.
   - `def is_thinking(self) -> bool`: State check.
3. **Refactor**: Remove lines 349-358 in `orchestrator_brain.py` and replace with `ThinkingEngine` calls.

## Acceptance Criteria
- [ ] `core/modules/thinking.py` exists.
- [ ] `orchestrator_brain.py` is reduced in complexity.
- [ ] Thoughts still appear in the UI.
