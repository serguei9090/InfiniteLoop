---
name: code-gap-reviewer
description: Specialized auditing skill for identifying discrepancies between project specifications (AGENTS.md, rules, docs/) and the actual codebase implementation. Use this for architectural audits and logic-gap discovery.
---

# Code Gap Reviewer Skill

This skill provides a systematic workflow for auditing the codebase against its intended design and identifying "gaps"—missing logic, incorrect implementations, or architectural drifts.

## 1. Audit Workflow

1.  **Identify the Source of Truth**: Read the relevant specifications (e.g., project rules in `.agents/rules/` and core documentation).
2.  **Scan the Implementation**: Use `grep_search` and `list_directory` to locate the current implementation of the features or architectural patterns.
3.  **Perform the Gap Analysis**:
    - **Missing Logic**: Does the code implement all requirements defined in the spec?
    - **Spec Discrepancy**: Does the implementation follow the architectural laws (e.g., SoC, DI)?
    - **Interface Drift**: Do the actual interfaces match the "Contract" defined in the planning phase?
4.  **Document Findings**: Update project tracking files with gaps, locations, impact, and remediation steps.

## 2. Best Practices for Gap Reviews

- **Be Critical**: Do not assume the code is correct just because it runs. Verify it against the project rules.
- **Traceability**: Every entry in the gap review should ideally link back to a specific requirement.
- **Actionable Output**: Always provide a clear path to closing the gap.

## 3. When to Use This Skill

- After a major feature implementation to verify architectural integrity.
- When onboarding to an existing codebase to map implementation discrepancies.
- During project "Check-points" or "Milestone Reviews."
