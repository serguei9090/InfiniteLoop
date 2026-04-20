# **Master Software Engineering Protocol**

Project Type: React Monorepo (Mobile/Desktop/Core)  
Architecture: Atomic Design (3-Tier)  
Methodology: TDD & CI/CD with Local Docker

### **Variable Definitions**
*   **`[PKG_MANAGER]`**: Generic placeholder. Replace with user selection: `npm`, `pnpm`, or `bun`.
*   **`[EXECUTE_CMD]`**: Generic placeholder. Replace with: `npx`, `pnpm dlx`, or `bunx`.
*   **`[LOCK_FILE]`**: `package-lock.json`, `pnpm-lock.yaml`, or `bun.lockb`.

### **Pre-Flight Protocol (Safety Interlock)**
**STOP!** Before executing any scaffolding instructions below, you **MUST** confirm the "Brain" is active:
1.  **Check Context:** Does `.agent/` exist?
2.  **Check Persona:** Does `AGENTS.MD` exist in the root?
3.  **Check Knowledge:** Is `ProDoc/documentation/product.md` populated with requirements?
    *   **IF NO:** Do NOT proceed. Go back and run `agentContext.md` hydration.
    *   **IF YES:** Proceed to Part 1.

## **PART 1: The Standards (Categorized Ruleset)**

### **1\. Architectural Standards (Atomic Design)**

* **Goal:** Maximum code reuse and visual consistency between React Native (Mobile) and React Web/Desktop.  
* **Structure:**  
  * **Tier 1: Design Tokens (The "X Files"):** Single source of truth for variables. No logic. (Colors, Typography, Spacing, Z-Index, Shadows, Radii, Elevation). Tokens live in `packages/ui/src/tokens`.  
  * **Tier 2: Primitive Components:** Pure functional components. They accept props for content but **never** define external margins or positioning. They handle platform specifics via file naming (`Component.tsx` + `Component.native.tsx`). Primitives live in `packages/ui/src/components`.  
  * **Tier 3: Feature/Page Layouts:** The logic layer. Defines positioning (Flexbox/Grid), margins, and data injection.  
* **Rule:** "Components define the *Interior*; Pages define the *Exterior*."

### **2\. Code Quality & Hygiene**

* **Linting & Formatting (Hybrid):** STRICT `Biome` enforcement. No ESLint/Prettier unless explicitly requested for legacy support.
* **Biome Config:**
  *   **Linter:** Enabled (Recommended constraints).
  *   **Formatter:** Enabled (Prettier compatible).
  *   **Import Sorting:** Enabled (Organization).  
* **Clean Code:**  
  * **DRY (Don't Repeat Yourself):** Logic used in more than two places moves to packages/core.  
  * **Descriptive Naming:** getUserById instead of getData.  
  * **Small Functions:** Functions should ideally do one thing.
* **UI vs Logic:** UI components are presentational and should not own business logic. Shared logic lives in core/services and is passed into UI via props/hooks.

### **3\. Testing Strategy (The "Test-First" Mandate)**

* **Methodology (TDD):**  
  1. **RED:** Write a failing unit test that describes the desired behavior *before* creating the function.  
  2. **GREEN:** Write the minimum code necessary to pass the test.  
  3. **REFACTOR:** Clean up the code while keeping the test green.  
* **Unit Tests (Web/Desktop):** `Vitest`. Fast, modern, compatible with Jest API.
* **Unit Tests (Mobile):** `Jest`. (Industry standard for React Native).
* **E2E / User Tests:** Playwright. Tests user flows (Login -> Dashboard -> Logout) in a real browser environment.
* **Code Coverage:** Minimum **80%** branch coverage required for passing the pipeline.

### **4\. Backend & Security**

* **Validation:** All inputs must be validated using a schema library (e.g., Zod) before processing.  
* **Authentication:** Stateless JWT or Session-based secure cookies.  
* **Architecture:** Controller-Service-Repository pattern to separate HTTP handling from Business Logic and Database Access.  
* **Security:**  
  * Sanitize all HTML outputs (XSS prevention).  
  * Use parameterized queries (SQL Injection prevention).  
  * Rate limiting on all public API endpoints.

### **5\. UI/UX Modern Best Practices**

* **Accessibility (a11y):** All interactive elements must have aria-labels and keyboard navigation support.  
* **Feedback:** Every user action (click, save, delete) requires immediate visual feedback (spinner, toast, or optimistic UI update).  
* **Mobile First:** Design layouts to be fluid. Avoid fixed pixel widths; use percentages or relative units (rem, flex).

### **6\. SDLC & CI/CD (Local Docker)**

* **Environment:** The entire build and test process runs inside a Docker container to ensure consistency (works on my machine \= works everywhere).  
* **Pipeline Stages:**  
  1. Lint & Static Analysis.  
  2. Unit Tests (Core Logic).  
  3. Build (Compilation check).  
  4. E2E Tests (Integration).  
  5. Report Generation.

## **PART 2: Agent Implementation Directives**

*Instructions for the AI Agent to generate specific infrastructure files based on the standards above.*

### **Directive 1: Setup Style Dictionary (Tokens)**

Task: Initialize the Token Build System.
Steps:
1.  **Install:** `[PKG_MANAGER] install -D style-dictionary` in `packages/ui`.
2.  **Source:** Create `packages/ui/tokens/src/custom/color.json`.
    ```json
    {
      "color": {
        "primary": { "value": "#0070f3" },
        "secondary": { "value": "#ff4081" }
      }
    }
    ```
3.  **Config:** Create `packages/ui/sd.config.js`.
    ```javascript
    module.exports = {
      source: ["tokens/src/**/*.json"],
      platforms: {
        js: {
          transformGroup: "js",
          buildPath: "tokens/dist/js/",
          files: [{ destination: "tokens.js", format: "javascript/module" }]
        },
        css: {
          transformGroup: "css",
          buildPath: "tokens/dist/css/",
          files: [{ destination: "variables.css", format: "css/variables" }]
        }
      }
    };
    ```
4.  **Build:** Run `[EXECUTE_CMD] style-dictionary build --config sd.config.js`.

### **Directive 2: Generate button.component.tsx (Tier 2\)**

Task: Create the standardized Button component for Desktop/Web.  
Requirements:

* Import tokens from Directive 1 (`import { tokens } from '../../tokens/dist/js/tokens'`).  
* Accept props: variant (primary/secondary), size, label, onClick, isLoading.  
* **Strict Rule:** No margin in the root styles.  
* Use TypeScript interfaces.  
* **Output File:** packages/ui/src/components/Button/Button.tsx (and .native.tsx counterpart).

### **Directive 3: Generate vitest.config.ts (Unit Testing)**

Task: Configure the Unit Test Runner (Web/Core).
Requirements:

*   **Config:** Use `defineConfig` from `vitest/config`.
*   **Environment:** `jsdom` (Simulate Browser).
*   **Coverage:** Enable v8 coverage, set threshold to 80%.
*   **Aliases:** Resolve `@/*` to `./src/*`.
*   **Output File:** `vitest.config.ts`

### **Directive 4: Generate playwright.config.ts (E2E Testing)**

Task: Configure the User Testing Runner.  
Requirements:

* Target the web build output.  
* Configure for Chromium, Firefox, and Mobile Safari (Webkit).  
* Set up a local web server command to run the app before testing.  
* Save screenshots/video on failure to /reports/e2e.  
* **Output File:** playwright.config.ts

### **Directive 5: Generate docker-compose.ci.yml (Local CI/CD)**

Task: Create a containerized pipeline environment.  
Requirements:

* Service ci-runner: Uses a Node.js image.  
* Volumes: Mount the local repo to the container.  
* Command: A script that runs the full workflow (Lint \-\> Test \-\> Build).  
* **Output File:** docker-compose.ci.yml

## **PART 2.5: Infrastructure Scaffolding Directives**

*CRITICAL: You MUST generate these files to initialize the physical project structure. Do not assume they exist.*

### **Directive 6: Scaffold Monorepo Root**

Task: Create the root configuration.
Requirements:
*   **Create File:** `package.json`
*   **Content:**
    ```json
    {
      "name": "monorepo-root",
      "private": true,
      "workspaces": ["apps/*", "packages/*"],
      "scripts": {
        "build": "[PKG_MANAGER] run build --workspaces",
        "test": "[PKG_MANAGER] run test --workspaces"
      }
    }
    ```
*   **Create File:** `tsconfig.base.json` (Standard React+Node config).

### **Directive 7: Scaffold Web App (apps/web)**

Task: Create the React Frontend.
Requirements:
*   **Create File:** `apps/web/package.json` (Deps: react, react-dom, vite, @ui/tokens).
*   **Create File:** `apps/web/vite.config.ts` (Standard Vite setup).
*   **Create File:** `apps/web/index.html` (Entry point pointing to src/main.tsx).
*   **Create File:** `apps/web/src/main.tsx` (React Root).
*   **Create File:** `apps/web/src/App.tsx` (Hello World component).

### **Directive 8: Scaffold UI Package (packages/ui)**

Task: Create the Shared UI Library.
Requirements:
*   **Create File:** `packages/ui/package.json`
    *   Name: `@pkg/ui`
    *   Main: `./src/index.ts`
    *   React Native: `./src/index.native.ts`
*   **Create File:** `packages/ui/src/index.ts` (Web Entry - Export web components).
*   **Create File:** `packages/ui/src/index.native.ts` (Native Entry - Export native components).
*   **Note:** Ensure strict separation of platform-specific code.

### **Directive 9: Generate biome.json (Root Linting)**

Task: Create the Universal Quality Config.
Requirements:
*   **Create File:** `biome.json`
*   **Content:**
    ```json
    {
      "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
      "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
      "formatter": { "enabled": true, "indentStyle": "space" },
      "organizeImports": { "enabled": true },
      "linter": { "enabled": true, "rules": { "recommended": true } }
    }
    ```

### **Directive 10: Configure TurboRepo (The Build System)**

Task: Set up the optimized build pipeline.
Requirements:
*   **Create File:** `turbo.json`
*   **Content:**
    ```json
    {
      "$schema": "https://turbo.build/schema.json",
      "pipeline": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": ["dist/**"]
        },
        "lint": {},
        "test": {},
        "dev": {
          "cache": false,
          "persistent": true
        }
      }
    }
    ```

## **PART 3: The Master Workflow File**

*This file references all rules and defines the execution order. Use this to orchestrate the SDLC.*

### **Workflow Definition: pipeline.workflow.yaml**

name: "Local CI/CD Pipeline"  
description: "Enforces Master Protocol standards before code commit."

variables:  
  REPORTS\_DIR: "./artifacts/reports"  
  COVERAGE\_DIR: "./artifacts/coverage"

stages:  
  \- name: "Sanity Check"  
    steps:  
      \- command: "[PKG_MANAGER] run lint"  
        description: "Checks code style and import sorting (Standard 2)."  
      \- command: "[PKG_MANAGER] run type-check"  
        description: "Verifies TypeScript integrity."

  \- name: "Logic Verification (TDD)"  
    steps:  
  \- name: "Logic Verification (TDD)"  
    steps:  
      \- command: "[PKG_MANAGER] run test:unit \-- \--coverage"  
        description: "Runs Unit tests. Fails if coverage \< 80% (Standard 3)."  
        output: "${COVERAGE\_DIR}/lcov-report/index.html"

  \- name: "Build Verification"  
    steps:  
  \- name: "Build Verification"  
    steps:  
      \- command: "[PKG_MANAGER] run build:core"  
      \- command: "[PKG_MANAGER] run build:web"  
        description: "Ensures the app compiles for desktop/web."

  \- name: "User Simulation (E2E)"  
    steps:  
  \- name: "User Simulation (E2E)"  
    steps:  
      \- command: "[PKG_MANAGER] run test:e2e"  
        description: "Runs Playwright scenarios against the built web app."  
        output: "${REPORTS\_DIR}/playwright-report"

  \- name: "Containerized Execution"  
    instruction: "Run the following command to execute all above steps in isolation:"  
    command: "docker-compose \-f docker-compose.ci.yml up \--abort-on-container-exit"

### **Protocol Checklist for Developers**

1. \[ \] Did you write the test **before** the code?  
2. \[ \] Did you use Design Tokens instead of hardcoded hex values?  
3. \[ \] Does your component have zero external margins?  
4. \[ \] Did you run the Docker CI locally before pushing?

## **PART 4: Initialization Protocol**

*Run these commands to bring the "Body" (Project) and "Brain" (Context) to life.*

### **Phase 1: System Prep**
1.  **Version Control:**
    *   `git init`
    *   `touch .gitignore` (Population: `node_modules`, `.env`, `coverage`, `dist`, `__pycache__`, `.DS_Store`).
2.  **Environment:**
    *   `touch .env` (Add `VITE_API_URL=http://localhost:8000`).
3.  **Planning Infrastructure:**
    *   `mkdir -p .agent/plans/active`
    *   `mkdir -p .agent/plans/archive`
    *   `touch .agent/plans/fastPlan.md`
    *   `touch .agent/plans/plan_history_log.md`

### **Phase 2: Dependency Injection**
1.  **Frontend/Root:** `[PKG_MANAGER] install`

### **Phase 3: QA & DX Setup (The Safety Net)**
1.  **Lefthook (Orchestrator):**
    *   Install: `[PKG_MANAGER] install -D lefthook`
    *   Config: Create `lefthook.yml`.
        ```yaml
        pre-commit:
          parallel: true
          commands:
            biome:
              glob: "*.{js,ts,tsx,jsx,json,css}"
              run: [EXECUTE_CMD] biome check --write --no-errors-on-unmatched {staged_files} && [PKG_MANAGER] run build
            test:
              glob: "*.{ts,tsx}"
              run: [EXECUTE_CMD] vitest related --run {staged_files}
        ```
2.  **Editor Config (VS Code):**
    *   Generate `.vscode/settings.json` with:
        ```json
        {
          "editor.formatOnSave": true,
          "editor.defaultFormatter": "biomejs.biome"
        }
        ```
    *   Generate `.vscode/extensions.json` recommending `biomejs.biome`.

### **Phase 4: Testing Infrastructure**
1.  **Vitest Injection:**
    *   Install: `[PKG_MANAGER] install -D vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom jsdom`
    *   Setup: Create `apps/web/src/test/setup.ts` { import '@testing-library/jest-dom'; }
    *   Create a dummy test `apps/web/src/App.test.tsx` to confirm the runner passes.

### **Phase 5: Scripts & Orchestration (Monorepo Powers)**
1.  **Turbo Injection:**
    *   Add scripts to root `package.json`:
        *   `"dev": "turbo run dev"`
        *   `"build": "turbo run build"`
        *   `"lint": "turbo run lint"`
        *   `"test": "turbo run test"`
        *   `"clean": "rm -rf node_modules **/**/node_modules"`
