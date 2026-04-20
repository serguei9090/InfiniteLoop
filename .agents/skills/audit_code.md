# Skill: Audit Code

## Objective
Your goal as the QA/Test Engineer (@qa-tester) is to aggressively review the newly generated code to guarantee production-readiness.

## Rules of Engagement
- **Target Context**: The `/src` folder, routing files, and all dependency scripts.
- **The 3-Strike Rule**: If you attempt to fix a linting error or test failure 3 times and it still fails, you must STOP execution and generate an incident report in `docs/reports/`.

## Instructions
1. **Assess Parity**: Validate that the code properly implements the features defined in `docs/architecture/Technical_Specification.md`.
2. **Bug Hunting**: Actively search for:
   - Missing module imports.
   - Unhandled promises and thread-safe data blocking (e.g. DuckDB WAL).
   - Python type mismatch (using `ruff`).
   - JS/TS formatting issues (using `biome`).
3. **Commit Fixes**: Use your own editing tools to rewrite the flawed files. Ensure everything is passing before exiting.
