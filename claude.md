# Claude Code / Gemma-4 Thinking Mode Guidelines
## Purpose
This document guides the integration of internal reasoning mechanisms ("Thinking Mode") into agentic workflows running on the Gemma 4 model. It defines how structured planning, self-correction, and step-by-step reasoning should be explicitly prompted to ensure predictable and traceable output.

## Enabling Thought Process (Chain-of-Thought / Planning)
To force a generative model into 'Thinking Mode' or explicit planning:

1.  **Prompt Structure:** Always use multi-step instructions that demand internal monologue before the final answer. Use phrases like "First, analyze X; Second, derive Y from X; Finally, provide Z."
2.  **Tool Schema Integration:** For tool calls, the model must be prompted to first output a *thought block* (e.g., `[THINKING]...[/THINKING]`) detailing which tools it will use and why, before generating the final structured JSON or code block that uses those tools.
3.  **Self-Correction Loop:** Include instructions for self-correction: "After generating output, critically review your own result against Requirement Z. If discrepancies exist, rewrite the result."

## Key Directives for Gemma 4 Usage
*   **Constraint Adherence:** Always acknowledge and adhere to system constraints (e.g., security protocols, specific file formats, external APIs).
*   **Traceability:** All decisions must be traceable back to a prompt requirement or an observed failure state. The model must output its reasoning steps for debugging purposes.

## Implementation Example Prompt Snippet
"Given the user request and the existing codebase structure, first **[THINKING]**: Analyze file A's function signature vs B's API contract. Second, determine if a refactor is needed to solve X. Finally: [FINAL OUTPUT]"