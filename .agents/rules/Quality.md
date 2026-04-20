---
trigger: always_on
description: Mandatory standards for code quality, commenting, TODO management, and UI design.
---

# Code Quality & Documentation Standards

To ensure maximum clarity, maintainability, and consistent UI, all code must adhere to the following standards.

## 1. Zero-Guesswork Commenting Standard 
To maintain context for subagents across sessions, all files and structures must be thoroughly self-documenting.

- **Purpose (The Contract)**: 
  - Every file/module MUST have a header describing its goal.
  - Public interfaces must explicitly define: **Purpose** (What it does), **Args** (Inputs), **Returns** (Outputs), and **Faults** (Expected errors).
- **Variables/State**: Any non-obvious variable or state declaration must have a 1-line inline comment explaining *why* it exists.
- **Complex Logic**: If a block of logic is highly algorithmic or non-trivial, write a multi-line comment above it mapping out the steps in plain English before the code begins.

## 2. TODO(ID) Protocol (The "Task Memory")
Any incomplete interface, bypassed error, or missing feature MUST NOT be left as a silent placeholder. It MUST use the `TODO` keyword accompanied by a unique identifier.

- **The Formal TODO Syntax**: 
  - `// TODO(sync_001): [WHAT] Need to add debounce to this input. [WHY] API rate limits are being hit during fast typing.`
- **Creation Protocol (The "Detail File")**:
  1. **Assign a Unique ID**: (e.g., `api_gateway_001`).
  2. **Create the Brain**: Create a markdown file in `docs/TODOC/<unique_id>.md`. This is the **Active Task Memory**—include architectural choices, chosen libraries, logic snippets, and why we made those decisions.
  3. **Index the Task**: Add the high-level task to `docs/track/TODO.md`, linking to the detail file.

## 3. Pure TDD & Architectural BDD (Hybrid)
We distinguish between **Architectural Guidance** and **Implementation Speed**:
- **BDD (Gherkin)**: Use `.feature` files ONLY for high-level architectural contracts and user flows. This provides the "Living Spec" that mirrors your requirements.
- **Pure TDD**: During the intense implementation phase, we skip the Gherkin layer for specific unit logic. AI is faster with pure code definitions than English abstraction parsing.
- **The Flow**: Define Interface -> (Optional) Write Gherkin Feature for high-level flow -> Write isolated failing TDD spec -> Invoke `@jules-agent` -> Pass.


## 3. Atomic Design / Modular Structure
For any structured content or frontend components, the modular hierarchy must be strictly enforced:
- **Atoms**: Smallest functional units (e.g., base MD snippets, singular icons).
- **Molecules**: Groups of atoms functioning together (e.g., specific rules, combined snippets).
- **Organisms**: Complex sections (e.g., full workflow descriptions, headers).
- **Templates**: Page-level layouts focusing on content structure.
- **Pages**: Specific instances of templates populated with real data and state.
