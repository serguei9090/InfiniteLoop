# Development Orchestrator Memory

This directory contains persistent memory for the development orchestrator agent.

## Purpose

Store institutional knowledge about:
- User preferences and working style
- Project-specific patterns and conventions
- Architectural decisions and their rationale
- Known issues and workarounds
- Team feedback and corrections

## Memory Types

### user.md
Information about the user's role, goals, responsibilities, and technical expertise.

### feedback.md
Guidance from the user about how to approach work - both what to avoid and what to keep doing.

### project.md
Information about ongoing work, goals, initiatives, bugs, or incidents within the project.

### reference.md
Pointers to external systems where information can be found (e.g., Linear projects, Grafana dashboards).

## How to Use

When you discover important information:
1. Write it to the appropriate memory file using the frontmatter format
2. Add a pointer to MEMORY.md
3. Keep entries concise and up-to-date

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
