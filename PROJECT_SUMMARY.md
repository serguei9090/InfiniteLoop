# Immutable Core - Project Summary (v4.0)

## Overview
Immutable Core is an advanced autonomous development framework that utilizes AI to self-evolve, write code, and act as a backend engineer. The architecture has been refined to operate locally within tight resource constraints (e.g., RTX 3060 12GB VRAM) while utilizing powerful open-weight models like **Gemma 3 27B**.

## The Hybrid "Vibe-Coding" Stack (2026)
Since we are using local/open-weight models that often do not natively support strict JSON function calling via provider APIs (e.g., Gemini API rejecting tool payloads for Gemma 3), we have migrated to a robust **Hybrid Architecture** known as the "Holy Grail Stack":

1. **The Brain/State (Orchestration):** `core/modules/brain.py`
   - Orchestrates the loop. This will be extended to use **LangGraph** for long-term memory and SQLite checkpointing to survive VRAM crashes.
   - Manages dependencies and passes control between the Planner and the Executer.

2. **The Architect (Planning):** `core/modules/architect.py`
   - Powered by **PydanticAI**.
   - **Role:** High-level reasoning. It breaks a mission down into a strict `MissionPlan` consisting of `AtomicTasks`.
   - **Why PydanticAI?** Type-safety. It refuses to let the agent proceed unless the output perfectly matches the schema. If the model hallucinates or provides bad JSON, PydanticAI automatically loops back and corrects it.

3. **The Hands (Execution):** `core/modules/coder.py`
   - Powered by **SmolAgents (Hugging Face)**.
   - **Role:** The Surgical Coder. It picks up atomic tasks and executes them.
   - **Why SmolAgents?** Instead of brittle JSON ReAct loops, SmolAgents allows the model to write small Python snippets (edit scripts) to read files, edit lines, and run `pytest`. This text-to-code approach is highly native and reliable for open-source models.

4. **The Mission Control (Observation):**
   - A frontend React application (`ui/`) acting as a Generative UI Dashboard. You can monitor the system's health, AI evolution, and test pass rates without staring at terminal logs.

## Current Setup & Tooling
- **Proxy:** `litellm` is used locally on port 4000 to bridge standardized OpenAI client requests (from PydanticAI/SmolAgents) to the target model provider (e.g., Gemini).
- **Frontend Stack:** React, TypeScript, Tailwind CSS, shadcn/ui. (Code formatted and checked using `biome` and `tsc`).
- **Backend Stack:** Python, FastAPI, Pydantic, SmolAgents. (Tested using `pytest` with `pytest-cov` for coverage).
- **Core Loop:** The `cli/infinite.py` script serves as the primary entry point to launch evolution missions.
