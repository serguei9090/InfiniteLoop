# IMMUTABLE CORE

A fully autonomous, local-only coding agent capable of auto-evolving its own toolset without breaking its execution loop.

## Mission
Build a fully autonomous, local-only coding agent capable of auto-evolving its own toolset without breaking its execution loop. Must operate strictly within 12GB VRAM limits (targeting ~50 t/s) using Gemma-4 E4B/E2B (Multimodal) via local LM Studio.

## Technology Stack

- **Frontend UI/UX**: React (TypeScript), Tailwind CSS, shadcn/ui.
- **Frontend State**: Zustand.
- **Backend (Core)**: Python (FastAPI).
- **Data Validation**: Pydantic (Backend) / Zod (Frontend).
- **AI Orchestration**: Hybrid Stack (PydanticAI for Planning/Validation, SmolAgents for Execution).
- **API Proxy**: LiteLLM (bridges OpenAI schema to target models).
- **Local LLM Provider**: LM Studio (http://127.0.0.1:1234/v1).
- **Language**: TypeScript (Node/Bun) or Python.

## Core Modules

- **JIT Context Engine (Tree-Sitter)**: Parses the workspace using Tree-sitter on startup/file-change.
- **Guardrails & File Sandbox**: Jails all execution to the `./workspace` directory. Safe deletes route to `./workspace/.trash/`.
- **The Reflexion Loop (Auto-Retry)**: Catches malformed JSON or tool execution errors and feeds them back to the LLM.
- **Multimodal LLM Handler (Gemma-4)**: Supports base64 image ingestion and streams `<|think|>` tokens to a separate UI stream.
- **Auto-Evolution Engine (Tool Factory)**: AI writes new tool scripts + JSON schemas with automated validation.

## Directory Structure

```
./
├── .agents/                    # Core configuration and static rules
├── workspace/                  # The AI's sandbox - ALL AI work happens here
│   ├── .trash/                 # Where "deleted" files go
│   └── .agents/
│       └── dynamic_tools/      # AI-evolved toolsets
├── core/                       # The Immutable Core (FastAPI Backend)
│   ├── main.py                 # Entry point
│   ├── api/                    # API Endpoints for UI
│   ├── services/               # Business logic
│   ├── modules/                # Core subsystems
│   ├── schemas/                # Pydantic models
│   └── tests/                  # TDD test suites
└── ui/                         # Observer Dashboard (React + Vite)
```

For more detailed information, please refer to [ARCHITECTURE.md](ARCHITECTURE.md) and [FILE_STRUCTURE.md](FILE_STRUCTURE.md).
