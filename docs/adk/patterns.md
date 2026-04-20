# ADK 2.0 Implementation Patterns

This reference guide provides code snippets for transitioning LogLensAi components to the Google ADK standard.

## 1. Minimal Agent Definition

An `LlmAgent` replaces the manual system prompt management and loop control.

```python
from google.adk.agents.llm_agent import Agent

def workspace_explorer_agent():
    return Agent(
        name="workspace_explorer",
        description="Expert in analyzing project structure and reading files.",
        instruction="""
        You are a specialized explorer. 
        Your goal is to map the workspace and identify key logic files.
        Always start by listing the root directory.
        """,
        tools=[list_dir, read_file], # Tools are raw Python functions with docstrings
        model="gemini-2.0-flash" # Can be bridged to local via LiteLLM
    )
```

## 2. Docstring-Driven Tooling

Every tool MUST have a Google-style docstring for ADK to generate the JSON schema accurately.

```python
def read_file(path: str) -> dict:
    """
    Reads the content of a file from the workspace.

    Args:
        path: Absolute or relative path to the file.

    Returns:
        A dict with 'content' (str) or 'error' (str).
    """
    try:
        # Implementation...
        return {"content": "..."}
    except Exception as e:
        return {"error": str(e)}
```

## 3. Session & Runner Execution

The `Runner` handles the iterative loop until the agent signals completion.

```python
from google.adk.runners.loop_runner import LoopRunner

async def execute_mission(mission_text: str):
    agent = workspace_explorer_agent()
    runner = LoopRunner()
    
    # Run the mission
    result = await runner.run(agent, input_text=mission_text)
    
    return result
```

## 4. Multi-Agent Delegation

The true power of ADK is the ability for one agent to use another agent as a tool.

```python
# Primary agent can 'delegate' complex tasks
core_orchestrator = Agent(
    tools=[ui_agent_tool, backend_agent_tool],
    instruction="Orchestrate the feature implementation by delegating UI and Backend tasks."
)
```
