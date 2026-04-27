import json
from typing import List, Dict, Any


class ContextManager:
    def __init__(self, max_tokens: int = 4096, encoding_name: str = "cl100k_base"):
        self.max_tokens = max_tokens
        self.history: List[Dict[str, Any]] = []
        self._total_tokens = 0

        self._use_tiktoken = False
        try:
            import tiktoken
            self.encoding = tiktoken.get_encoding(encoding_name)
            self._use_tiktoken = True
        except ImportError:
            self.encoding = None

    def _count_tokens(self, content: Any) -> int:
        if self._use_tiktoken and self.encoding:
            try:
                if isinstance(content, str):
                    return len(self.encoding.encode(content, allowed_special="all"))
                elif isinstance(content, (dict, list)):
                    return len(self.encoding.encode(json.dumps(content), allowed_special="all"))
            except Exception:
                pass
        # Fallback to naive calculation
        return len(str(content)) // 4

    def _get_msg_tokens(self, msg: Dict[str, Any]) -> int:
        # A rough estimate for OpenAI chat format:
        # roughly 3 tokens per message + tokens for content
        tokens = 3
        for k, v in msg.items():
            if k not in ["_token_count"]:
                tokens += self._count_tokens(v)
        return tokens

    def add_message(self, role: str, content: Any, tool_call_id: str = None):
        msg = {"role": role}
        if isinstance(content, dict):
            msg.update(content)
        else:
            msg["content"] = content

        if tool_call_id:
            msg["tool_call_id"] = tool_call_id

        msg["_token_count"] = self._get_msg_tokens(msg)
        self.history.append(msg)
        self._total_tokens += msg["_token_count"]

        self._compress_if_needed()

    def _compress_if_needed(self):
        """
        Compression by removing the oldest non-system messages
        when estimated token count is too high.
        """
        target_tokens = int(self.max_tokens * 0.9)
        while self._total_tokens > target_tokens and len(self.history) > 3:
            removed_msg = self.history.pop(2)
            self._total_tokens -= removed_msg.get("_token_count", 0)

    def truncate_from_left(self, num_messages: int = 1):
        """
        Safely truncate older context messages from the left,
        preserving the system prompt (index 0) and initial task (index 1).
        """
        for _ in range(num_messages):
            if len(self.history) > 3:
                removed_msg = self.history.pop(2)
                self._total_tokens -= removed_msg.get("_token_count", 0)
            else:
                break

    def get_messages(self) -> List[Dict[str, Any]]:
        # Return messages without internal token tracking fields
        return [{k: v for k, v in m.items() if k != "_token_count"} for m in self.history]

    def set_system_prompt(self, prompt: str):
        if self.history and self.history[0]["role"] == "system":
            old_tokens = self.history[0].get("_token_count", 0)
            self.history[0]["content"] = prompt
            new_tokens = self._get_msg_tokens(self.history[0])
            self.history[0]["_token_count"] = new_tokens
            self._total_tokens += (new_tokens - old_tokens)
        else:
            msg = {"role": "system", "content": prompt}
            msg["_token_count"] = self._get_msg_tokens(msg)
            self.history.insert(0, msg)
            self._total_tokens += msg["_token_count"]

    def get_context_stats(self) -> Dict:
        return {
            "token_estimate": self._total_tokens,
            "message_count": len(self.history),
            "max_tokens": self.max_tokens,
        }

    def reset(self):
        """Reset the conversation history."""
        self.history = []
        self._total_tokens = 0
