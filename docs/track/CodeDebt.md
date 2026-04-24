# Code Debt Tracking

See full analysis in `project-report-2026-04-24.md § 4`.

## Active Debt
- `core/modules/auto_adaptation.py`: Nested `if` statements instead of single `if` (SIM102)
- `core/modules/context.py`: Nested `if` statements instead of single `if` (SIM102)
- `core/modules/evolution.py`: Nested `if` statements instead of single `if` (SIM102)
- `core/modules/multi_ai.py`: Uncapitalized environment variable `google_api` (SIM112)
- `core/modules/tool_registry.py`: Use of `.keys()` in dict check (SIM118)
- `core/services/context_manager.py`: Nested `if` statements instead of single `if` (SIM102)
- `core/services/tool_engine.py`: Missing ternary operator (SIM108)
- `ui/src/components/layout/FloatingMenu.tsx`: Logic duplication (jscpd clone)
