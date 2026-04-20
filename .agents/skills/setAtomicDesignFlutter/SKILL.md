---
name: Set Atomic Design
description: Enforce Atomic Design principles and project structure checks for the Flutter project.
---

# Atomic Design & Architecture Verification

This skill aligns the agent with the project's Very Good CLI architecture refactored into Atomic Design.

## 1. Context Analysis
You must understand the current Atomic status before generating code.
- **Action**: Scan the `lib/` folder to understand the current Atomic structure (atoms, molecules, pages).

## 2. Coding Standards
Strictly adhere to `very_good_analysis` lints:
- **Const**: ALWAYS use `const` constructors where possible.
- **Types**: ALWAYS use explicit types.
- **Formatting**: ALWAYS use trailing commas.

## 3. The Golden Rule of Reuse
**Constraints**:
- Before generating any new UI code, you **MUST** check `lib/ui/atoms` and `lib/ui/molecules`.
- If a component (like a button or text style) exists, **reuse it**.
- **Do not** create raw `ElevatedButton` or `Text` widgets inside pages if a wrapped component exists.

## 4. Project Structure Context
- **UI Components**: `lib/ui/`
- **Business Logic**: `lib/logic/` (Cubits/Blocs)
- **Entry Point**: `lib/app/`
