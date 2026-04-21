from typing import List, Dict, Any


class ContextManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: Any, tool_call_id: str = None):
        msg = {"role": role}
        if isinstance(content, dict):
            msg.update(content)
        else:
            msg["content"] = content

        if tool_call_id:
            msg["tool_call_id"] = tool_call_id

        self.history.append(msg)
        self._compress_if_needed()

    def _compress_if_needed(self):
        """
        Naive compression by removing the oldest non-system messages
        when estimated token count is too high.
        """
        # Very rough estimation: 1 token ~= 4 characters
        total_chars = 0
        for m in self.history:
            content = m.get("content", "")
            if isinstance(content, str):
                total_chars += len(content)
            elif isinstance(content, dict):
                total_chars += len(str(content))

            # Count tool calls if present
            if "tool_calls" in m:
                total_chars += len(str(m["tool_calls"]))

        token_estimate = total_chars // 4

        if token_estimate > (self.max_tokens * 0.9):
            # Keep system message (0) and Initial Mission (1)
            if len(self.history) > 3:
                # Remove eldest interaction (usually an assistant/user pair)
                # Starting at index 2 to preserve the root mission
                del self.history[2]
                self._compress_if_needed()  # Recurse if still too big

    def truncate_from_left(self, num_messages: int = 1):
        """
        Safely truncate older context messages from the left,
        preserving the system prompt (index 0) and initial task (index 1).
        """
        for _ in range(num_messages):
            if len(self.history) > 3:
                del self.history[2]
            else:
                break

    def get_messages(self) -> List[Dict[str, Any]]:
        return self.history

    def set_system_prompt(self, prompt: str):
        if self.history and self.history[0]["role"] == "system":
            self.history[0]["content"] = prompt
        else:
            self.history.insert(0, {"role": "system", "content": prompt})

    def get_context_stats(self) -> Dict:
        total_chars = 0
        for m in self.history:
            content = m.get("content", "")
            total_chars += len(str(content))
            if "tool_calls" in m:
                total_chars += len(str(m["tool_calls"]))

        return {
            "token_estimate": total_chars // 4,
            "message_count": len(self.history),
            "max_tokens": self.max_tokens,
        }

    def reset(self):
        """Reset the conversation history."""
        self.history = []
