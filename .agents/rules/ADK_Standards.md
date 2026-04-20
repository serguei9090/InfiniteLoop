---
trigger: always_on
---
# Google ADK 2.0 Standards

All agents and sub-agents operating in the InfiniteLoop ecosystem MUST adhere to the following standards to ensure compatibility with the **Google Agent Development Kit (ADK) 2.0**.

## 1. Docstring-Driven Tooling
Every tool (Python function or class) MUST have a Google-style docstring. This is the **primary source of truth** for ADK's automatic JSON schema generation.

### Example:
```python
def my_tool(param: str) -> dict:
    """
    Description of the tool.

    Args:
        param: Description of the parameter.

    Returns:
        A dict containing 'success' and 'data'.
    """
    return {"success": True, "data": "..."}
```

## 2. Orchestration via Runner
Direct manual loops (while/for) for agent orchestration are FORBIDDEN. All multi-turn interactions MUST be managed by a `google.adk.runners.Runner` instance.

## 3. Modular Agent Definition
Agents should be defined as standalone instances of `google.adk.Agent`. One agent should never directly call another agent's internal methods; instead, it should use the other agent as a **Tool**.

## 4. State Isolation
Agents must remain stateless between missions. any persistent state must be saved to the database or workspace files via the providing tools.
