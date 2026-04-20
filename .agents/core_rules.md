---
trigger: always_on
---
# IMMUTABLE CORE - Execution Rules

1. **Immutable Core**: You MUST NOT modify any files in the `core/` directory unless specifically instructed to refactor the core itself. Your primary workspace is `./workspace/`.
2. **Path Safety**: Use the `WorkspaceGuard` (when implemented) for all file operations. Never use absolute paths outside of `./workspace/`.
3. **Stream Protocol**: All output must be wrapped in `<|think|>` tags for internal reasoning, and outside of them for tool calls or user communication.
4. **Tool Evolution**: If you need a capability that doesn't exist, use `create_new_tool` to evolve.
5. **No RAG**: Rely on the JIT Context Engine (Tree-sitter skeleton) for codebase awareness. do not attempt to use embeddings.
6. **VRAM Efficiency**: Keep context compressed. Strip non-essential formatting from injected code snippets.
