"""
LLM Bridge - Unified LLM Interface
PURPOSE: Provide a standardized way to interact with local/remote LLMs.
CONTRACT:
- chat_stream(messages, ...): Async generator for streaming completions.
- chat_complete(messages, ...): Standard completion call.
"""

from typing import AsyncGenerator, List, Dict, Optional
from openai import AsyncOpenAI
from config import settings

class LLMBridge:
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        model: str = None,
    ):
        self.base_url = base_url or settings.llm_base_url
        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model
        self.client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key)

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream responses from the LLM.
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = tool_choice

            stream = await self.client.chat.completions.create(**kwargs)
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    yield delta.model_dump()
        except Exception as e:
            yield {"content": f"Error in LLM Bridge: {str(e)}"}

    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ) -> Dict:
        """
        Standard completion call.
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": False,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = tool_choice

            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.model_dump()
        except Exception as e:
            return {"content": f"Error in LLM Bridge: {str(e)}"}
