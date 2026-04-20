# IMMUTABLE CORE Architecture Specification

## Mission
Build a fully autonomous, local-only coding agent capable of auto-evolving its own toolset without breaking its execution loop. Must operate strictly within 12GB VRAM limits (targeting ~50 t/s) using Gemma-4 E4B/E2B (Multimodal) via local LM Studio.

## Technology Stack (Strictly Enforced)

- **Frontend UI/UX**: React (TypeScript), Tailwind CSS, shadcn/ui.
- **Frontend State**: Zustand.
- **Backend (Core)**: Python (FastAPI).
- **Data Validation**: Pydantic (Backend) / Zod (Frontend).
- **AI Orchestration**: Google Gen AI SDK (compatible with OpenAI spec).
- **Local LLM Provider**: LM Studio (http://127.0.0.1:1234/v1).
- **Language**: TypeScript (Node/Bun) or Python.

## Engineering & Architecture Rules

- **TDD is MANDATORY**: Write failing unit test first, then minimal code, then refactor.
- **Frontend Architecture**: Atomic Design (Atoms, Molecules, Organisms, Pages).
- **Styling**: Tailwind CSS exclusively. No custom CSS files.
- **UI Components**: shadcn/ui.
- **Backend Architecture**: Strict separation (Routers -> Services -> Data Access).
- **API Contract**: `{ "success": boolean, "data": any, "error": string | null }`.

## Core Modules

### A. JIT Context Engine (Tree-Sitter)
- Parse `./workspace` using Tree-sitter on startup/file-change.
- Store AST graph in memory (classes, function signatures, types).
- **Rule**: NO RAG. NO EMBEDDINGS.
- **Compression**: Strip docstrings/comments/whitespace before injecting context. Send "skeleton" by default. Full bodies only via explicit tool call.

### B. Guardrails & File Sandbox
- Jail all execution to `./workspace`.
- Block any path containing `../` escaping root.
- **Safe Delete**: AI cannot `rm`. Route deletes to `./workspace/.trash/`.

### C. The Reflexion Loop (Auto-Retry)
- Catch malformed JSON or tool execution errors (stderr).
- Feed stderr back to LLM for fixing.
- **Circuit Breaker**: Max 3 retries per action. Rollback if failed >3 times.

### D. Multimodal LLM Handler (Gemma-4)
- Support base64 image ingestion in tool returns.
- **Stream Parsing**: Intercept `<|think|>` tokens. Route monologue to separate UI stream.

### E. Auto-Evolution Engine (Tool Factory)
- AI writes new tool scripts + JSON schemas to `./workspace/.agents/dynamic_tools/`.
- **Automated Validation**: Syntax Pass, Schema Compliance, Security Scan, Timeout Bound, I/O Dry-Run.

## File Structure Mandate

```
./
├── .agents/                    # Evolution & agent rules
├── workspace/                  # AI working directory (Sandboxed)
│   ├── .trash/                 # Safe delete target
│   └── .agents/
│       └── dynamic_tools/      # Self-generated tools
├── core/                       # Immutable Core (Python/FastAPI)
│   ├── main.py
│   ├── modules/
│   │   ├── thinking.py         # Stream parsing & monologue
│   │   ├── context.py          # Tree-sitter engine
│   │   ├── sandbox.py          # Path validation & guardrails
│   │   └── tools/              # Base tool definitions
│   └── evolution/              # Tool validation & registration
└── ui/                         # Minimal Observer UI (React)
```