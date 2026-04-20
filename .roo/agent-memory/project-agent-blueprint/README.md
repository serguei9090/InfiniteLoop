# Project Agent Blueprint Memory

This directory contains persistent memory for the project agent blueprint agent.

## Purpose

Store institutional knowledge about:
- Project requirements and constraints
- Architectural patterns and decisions
- Technical standards and conventions
- Tooling and infrastructure needs

## Memory Types

### user.md
Information about the user's role, goals, responsibilities, and technical expertise relevant to project architecture.

### feedback.md
Guidance from the user about architectural preferences, tooling choices, and what approaches work well.

### project.md
Information about ongoing initiatives, technical debt, and project-specific context.

### reference.md
Pointers to external resources, documentation, or systems relevant to the project architecture.

## How to Use

When analyzing project requirements:
1. Document key architectural decisions
2. Record user preferences for tools and patterns
3. Note constraints and limitations discovered
4. Track evolving understanding of the domain

## Memory Files Structure

Each memory file should have this structure:

```markdown
---
name: {{memory name}}
description: {{one-line description}}
type: {{user, feedback, project, reference}}
---

{{memory content}}
```

## MEMORY.md Index

The MEMORY.md file is an index that points to all memory files. Each entry should be one line under ~150 characters.
