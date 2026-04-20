# Google Agent Development Kit (ADK) 2.0 Integration

This document outlines the standard for using the Google ADK SDK within the InfiniteLoop / LogLensAi ecosystem.

## 📦 Package Information
- **Official Package**: `google-adk`
- **GitHub**: `https://github.com/google/adk-python`
- **Documentation**: `https://google.github.io/adk-docs/`

## 🧩 Core Components

| Component | Description | Implementation Goal |
| :--- | :--- | :--- |
| **`Agent`** | The reasoning entity. Defines instructions, tools, and model. | Replace `OrchestratorBrain`'s custom prompt handling. |
| **`Runner`** | Manages the execution loop and session state. | Replace `_run_orchestration_loop` in `OrchestratorBrain`. |
| **`SessionService`** | Handles state persistence. | Integrated with LogLensAi's DuckDB backend. |
| **`BuiltInPlanner`** | Handles multi-step reasoning. | Native replacement for our thinking engine protocol. |

## 🛠️ Tooling Standard (ADK 2.0)

ADK 2.0 uses **Docstring-Driven Tooling**. Every tool must follow this rigid structure:

```python
def my_tool(param1: str, param2: int) -> dict:
    """
    Clear and concise description of the tool.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        A dict containing 'status' and the result data.
    """
    # implementation
    return {"status": "success", "data": ...}
```

## 🔄 Transition Plan: Custom -> ADK

1. **Phase 1: Environment Readiness**: Install `google-adk` via `uv add google-adk`.
2. **Phase 2: Tool Migration**: Refactor `BaseTools` and `DynamicTools` to use the docstring-driven format.
3. **Phase 3: Brain Refactor**:
    - Replace `OrchestratorBrain` with an `LlmAgent` instance.
    - Connect `LlmAgent` to our local LLM via the `OpenAIChatModel` or `LiteLLM` bridge.
4. **Phase 4: Dashboard Integration**: Use `adk web` or custom events to feed the LogLensAi dashboard.

## 🚀 Why ADK?
- **Graph-based stability**: Prevents the reasoning loops we encountered with custom implementations.
- **Observability**: Built-in tracing for "Thoughts" and "Actions".
- **Scalability**: Native support for multi-agent delegation (e.g., a "Core" agent delegating to a "UI" agent).
