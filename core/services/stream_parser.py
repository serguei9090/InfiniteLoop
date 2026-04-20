from typing import AsyncGenerator, Tuple


class StreamParser:
    def __init__(self):
        self.in_thinking_block = False
        self.buffer = ""
        self.think_start_tag = "<|think|>"
        self.think_end_tag = "</|think|>"  # Assuming a closing tag or similar

    async def parse(
        self, stream: AsyncGenerator[str, None]
    ) -> AsyncGenerator[Tuple[str, bool], None]:
        """
        Yields (content, is_thinking)
        """
        async for chunk in stream:
            self.buffer += chunk

            while True:
                if not self.in_thinking_block:
                    if self.think_start_tag in self.buffer:
                        # Found start tag
                        pre_content, post_content = self.buffer.split(
                            self.think_start_tag, 1
                        )
                        if pre_content:
                            yield pre_content, False
                        self.in_thinking_block = True
                        self.buffer = post_content
                        continue
                    else:
                        # No start tag found yet, yield what we have if it couldn't be a partial tag
                        # To handle partial tags at the end of buffer, we keep the last few chars
                        safe_len = len(self.think_start_tag) - 1
                        if len(self.buffer) > safe_len:
                            to_yield = self.buffer[:-safe_len]
                            self.buffer = self.buffer[-safe_len:]
                            if to_yield:
                                yield to_yield, False
                        break
                else:
                    if self.think_end_tag in self.buffer:
                        # Found end tag
                        thought_content, post_content = self.buffer.split(
                            self.think_end_tag, 1
                        )
                        if thought_content:
                            yield thought_content, True
                        self.in_thinking_block = False
                        self.buffer = post_content
                        continue
                    else:
                        # No end tag found yet
                        safe_len = len(self.think_end_tag) - 1
                        if len(self.buffer) > safe_len:
                            to_yield = self.buffer[:-safe_len]
                            self.buffer = self.buffer[-safe_len:]
                            if to_yield:
                                yield to_yield, True
                        break

        # Final flush
        if self.buffer:
            yield self.buffer, self.in_thinking_block
