---
name: react-context-standard-v2
description: Deploys the React Context Standard V2 files and structure to a project. Use this skill when the user wants to set up a new React project with the V2 standard, or when they ask to "deploy standard v2", "setup agent project", or "initialize context standard".
---

# React Context Standard V2

This skill provides the standard operating procedures and context files for setting up a React project with the "Agentic Governance Framework" V2 standard.

## Usage

Follow these steps to deploy the standard:

### 1. Requirements Analysis
First, ensure you have read the user's project requirements. If `ProDoc/documentation/product.md` does not exist, ask the user for requirements or create it based on their prompt.

### 2. Context Injection
Use the file `references/agentContext.md` to guide the creation of the `.agent` directory and its contents.
- The `assets/Context` directory in this skill contains the source files for `.agent/rules` and `.agent/workflows`.
- **Copy** `assets/Context/rules` to `.agent/rules`.
- **Copy** `assets/Context/workflows` to `.agent/workflows`.
- Follow the "Customization & Hydration" steps in `references/agentContext.md` to create `AGENTS.MD` and `ProDoc` structure.

### 3. Project Scaffolding
Use the file `references/agentProjectSetup.md` to scaffold the project structure.
- It contains instructions for:
  - Directory structure (`apps/`, `packages/`)
  - Configuration files (`package.json`, `tsconfig.json`, `biome.json`, `turbo.json`)
  - CI/CD setup (`docker-compose.yml`, `pipeline.workflow.yaml`)

### 4. Verification
After deployment, verify:
- `.agent` folder exists with `rules` and `workflows`.
- `AGENTS.MD` exists in the root.
- `ProDoc/documentation/product.md` exists.
- `package.json` and other config files are created.
