# .roo - Roo Agent Instructions Folder

This folder contains agent instruction files and workflows for the roocode AI assistant.

## Purpose

The `.roo` directory mirrors the agent instruction structure from other AI assistants (`.claude`, `.gemini`) to provide roocode with:
- Agent definitions and roles
- Governance rules
- Prompt templates
- Memory storage locations

## Folder Structure

```
.roo/
├── README.md                    # This file - documentation for the folder
├── agents/                      # Agent definition files
│   ├── development-orchestrator.md  # Full-stack development lifecycle agent
│   ├── project-agent-blueprint.md   # Project architecture and blueprint agent
│   ├── core-evolution-agent.md      # Backend evolution and hardening agent
│   └── ui-hardener-agent.md         # Frontend polishing and UI agent
├── agent/                       # Shared agent resources (Gemini-style)
│   ├── governance/              # Governance rules and policies
│   │   └── rules.json           # JSON-based governance rules
│   └── prompts/                 # Prompt templates
│       ├── system.txt           # System prompt for orchestrator
│       ├── surgical_edit.txt    # Surgical edit operation template
│       └── summarize.txt        # Context summarization template
└── agent-memory/               # Memory storage locations
    ├── development-orchestrator/     # Memory for development orchestrator
    │   └── README.md
    └── project-agent-blueprint/      # Memory for project blueprint
        └── README.md
```

## Agent Descriptions

### development-orchestrator
Manages complex, multi-disciplinary software development lifecycles. Executes a 7-phase development cycle:
1. Feature & Design (Vision)
2. Planning & Scoping (Blueprint)
3. Critique & Plan Review (Peer Check)
4. Coding & Implementation (Build)
5. Linting & Formatting (Polish)
6. Unit Testing (Validation)
7. Final Review & Polish (Gatekeeper)

### project-agent-blueprint
Analyzes project requirements and generates blueprints for specialized agent suites. Acts as a system designer, not a coder. Specializes in:
- Architecture planning
- Code review specifications
- Test case generation
- Documentation creation

### core-evolution-agent
Handles backend evolution cycles with focus on:
- Safety-first modifications
- Atomic edits
- Verification and testing
- FastAPI, uv, and pydantic expertise

### ui-hardener-agent
Manages frontend polishing and component lifecycle:
- Visual excellence (Glassmorphism, Lucide-React, Tailwind)
- Quality gating with biome checks
- Component reliability
- Hydration safety

## Governance Rules

The `agent/governance/rules.json` file contains rules for agent behavior:
- Safety-first operations
- Minimal changes principle
- No secrets in code
- Document all changes
- Resource-aware operations
- Test-first development
- Code quality standards

## Prompt Templates

Located in `agent/prompts/`:
- **system.txt**: Main orchestrator system prompt
- **surgical_edit.txt**: Template for precise file modifications
- **summarize.txt**: Context summarization guidelines

## Memory System

The `agent-memory/` folder provides persistent memory locations for agents. Each agent has its own subfolder with:
- README.md explaining the memory system
- Subfolders for different memory types (user, feedback, project, reference)
- MEMORY.md index file (to be populated as memories are added)

## Usage

When roocode needs to:
1. **Understand an agent's role**: Read the corresponding `.md` file in `agents/`
2. **Apply governance rules**: Reference `agent/governance/rules.json`
3. **Use prompt templates**: Check `agent/prompts/` for format examples
4. **Store memory**: Write to appropriate files in `agent-memory/`

## Notes

- This folder is version-controlled and shared across sessions
- Memory files should be updated as the user provides feedback or new information is discovered
- The structure mirrors Claude Code and Gemini agent conventions for consistency
