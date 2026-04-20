---
trigger: always_on
---
# IMMUTABLE CORE: Architectural Separation & Isolation Law

To ensure the stability of the autonomous engine, all agents MUST adhere to the following preservation guardrails.

## 1. Core Immutability
The following directories and files are considered the **IMMUTABLE CORE** of the project. Any modification to these requires EXPLICIT user confirmation and is generally forbidden during feature-expansion missions:
- `core/services/loop_orchestrator.py`: The central loop logic.
- `core/services/tool_engine.py`: The tool dispatch engine.
- `core/modules/base_tools.py`: The low-level filesystem interfaces.
- `core/modules/sandbox.py`: The security guardrail implementation.

## 2. Extension via Plugins & Middleware
New features (Dashboards, APIs, Tools) MUST be implemented using the **Extension Pattern**:
- **API Extensions**: Create new files in `core/modules/` (e.g., `dashboard_router.py`) and use `APIRouter`. Include these into `main.py` using `.include_router()`.
- **Dynamic Tools**: Use the `create_new_tool` interface to evolve capabilities without modifying the core tool list.
- **UI Features**: Implement new views in `ui/src/features/` rather than modifying `App.tsx` directly.

## 3. Directory Protocol
- `core/workspace/`: This is the agent's safe playground. MISSION output files should be generated here.
- `core/plugins/`: Dedicated folder for third-party or subagent-generated extensions.

## 4. Rationale
By maintaining a static core and dynamic extension layer, we ensure that the orchestrator can continue to upgrade its own dashboard and capabilities without "decapitating" itself (modifying the logic that allows it to edit code).
