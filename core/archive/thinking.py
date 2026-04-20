"""
Thinking Engine - Stream Parsing and Monologue Management
Intersects LLM output streams to extract thoughts and monologue.
"""

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class ThinkingEngine:
    """
    Manages the 'thinking' state of the LLM stream.
    Identifies <|think|> and <|/think|> tags and extracts the monologue.
    """
    
    def __init__(self):
        self.is_thinking = False
        self.current_thought = ""
        self.monologue_buffer = ""
        self.thinking_tag_start = "<|think|>"
        self.thinking_tag_end = "<|/think|>"

    def process_chunk(self, chunk: str) -> Tuple[str, Optional[str]]:
        """
        Processes a stream chunk.
        
        Returns:
            A tuple of (clean_version_of_chunk, optional_thought_emitted)
        """
        self.monologue_buffer += chunk
        
        # Check for start tag
        if not self.is_thinking and self.thinking_tag_start in self.monologue_buffer:
            self.is_thinking = True
            # Find the position after the tag
            start_idx = self.monologue_buffer.find(self.thinking_tag_start)
            before_tag = self.monologue_buffer[:start_idx]
            after_tag = self.monologue_buffer[start_idx + len(self.thinking_tag_start):]
            
            self.monologue_buffer = after_tag
            self.current_thought = after_tag
            return before_tag, after_tag

        # Check for end tag
        if self.is_thinking:
            if self.thinking_tag_end in chunk:
                self.is_thinking = False
                end_idx = chunk.find(self.thinking_tag_end)
                content_before_end = chunk[:end_idx]
                content_after_end = chunk[end_idx + len(self.thinking_tag_end):]
                
                self.current_thought += content_before_end
                thought_to_return = content_before_end
                
                # Reset buffer and return clean remaining chunk
                self.monologue_buffer = content_after_end
                return content_after_end, thought_to_return
            else:
                self.current_thought += chunk
                return "", chunk
        
        # If not thinking and no tag found yet, just return the chunk
        return chunk, None

    def reset(self):
        """Reset state for a new stream."""
        self.is_thinking = False
        self.current_thought = ""
        self.monologue_buffer = ""
