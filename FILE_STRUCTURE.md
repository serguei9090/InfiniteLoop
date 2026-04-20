# IMMUTABLE CORE - Directory Structure

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
│   │   ├── llm_bridge.py       # LM Studio connector
│   │   ├── stream_parser.py    # <|think|> block extractor
│   │   ├── context_engine.py   # Tree-sitter integration
│   │   └── loop_orchestrator.py # Observe-Think-Act loop
│   ├── modules/                # Core subsystems
│   │   ├── sandbox.py          # Path guardrails
│   │   ├── base_tools.py       # Initial capabilities
│   │   └── evolution.py        # Tool factory & validator
│   ├── schemas/                # Pydantic models
│   └── tests/                  # TDD test suites
└── ui/                         # Observer Dashboard (React + Vite)
    ├── src/
    │   ├── components/         # Atomic Design folders
    │   │   ├── atoms/
    │   │   ├── molecules/
    │   │   └── organisms/
    │   ├── store/              # Zustand state
    │   └── App.tsx
    ├── package.json
    └── tailwind.config.js
```