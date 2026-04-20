---
trigger: manual
description: Standard for project progress tracking and documentation management.
---

# Project Tracking Standards

To maintain a clear and professional project roadmap, the following tracking files must be maintained inside `docs/track/`:

## 1. Tracking Files
- **`TODO.md`**: Main active roadmap. Tracks current phases, roadmap items, and completed milestones. 
- **`FeaturesProposal.md`**: Deferred features, ideas, and post-MVP enhancements.
- **`CodeDebt.md`**: Technical debt, refactoring needs, and known bugs.
- **`codegapreview.md`**: Architectural implementation gaps, missing logic, and spec discrepancies.

## 2. Maintenance Protocol
- **Single-Source Roadmap**: The agent manages project tasks directly in `docs/track/TODO.md`. System Artifacts are used for transient logging, not roadmap syncing.
- **Post-Feature Update**: After completing any task or feature, the agent MUST update `docs/track/TODO.md` by marking the item as `[x]`. 
- **Debt Identification**: If technical debt is introduced or discovered during development, it must be documented immediately in `CodeDebt.md`.
- **Feature Requests**: New feature ideas mentioned by the user or identified during planning should be added to `FeaturesProposal.md` if they are not part of the current active sprint.
- **Status Reporting**: Always reference the status of these files when providing progress summaries to the user.

## 3. Directory Integrity
- All tracking files MUST live in `docs/track/`.
- Redundant tracking files in the root or `docs/` should be consolidated and removed.
