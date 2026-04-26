import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.llm_bridge import LLMBridge


@pytest.mark.asyncio
async def test_chat_complete():
    """Verify that chat_complete calls OpenAI client correctly."""
    with patch("services.llm_bridge.AsyncOpenAI") as MockClient:
        # Mock instance
        client_instance = MockClient.return_value
        # Mock completions.create as async
        client_instance.chat.completions.create = AsyncMock()

        # Mock response structure - model_dump is sync
        mock_message = MagicMock()
        mock_message.model_dump.return_value = {"content": "hello", "role": "assistant"}

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        client_instance.chat.completions.create.return_value = mock_response

        bridge = LLMBridge()
        response = await bridge.chat_complete([{"role": "user", "content": "hi"}])

        assert response["content"] == "hello"
        client_instance.chat.completions.create.assert_called_once()
        kwargs = client_instance.chat.completions.create.call_args.kwargs
        assert kwargs["stream"] is False
        assert kwargs["messages"][0]["content"] == "hi"


@pytest.mark.asyncio
async def test_chat_stream():
    """Verify that chat_stream yields chunks correctly."""
    with patch("services.llm_bridge.AsyncOpenAI") as MockClient:
        client_instance = MockClient.return_value
        client_instance.chat.completions.create = AsyncMock()

        # Mock chunk generator
        async def mock_generator():
            # mock_delta.model_dump is sync
            mock_delta1 = MagicMock()
            mock_delta1.model_dump.return_value = {"content": "he"}

            mock_delta2 = MagicMock()
            mock_delta2.model_dump.return_value = {"content": "llo"}

            yield MagicMock(choices=[MagicMock(delta=mock_delta1)])
            yield MagicMock(choices=[MagicMock(delta=mock_delta2)])

        client_instance.chat.completions.create.return_value = mock_generator()

        bridge = LLMBridge()
        chunks = []
        async for chunk in bridge.chat_stream([{"role": "user", "content": "hi"}]):
            chunks.append(chunk)

        assert len(chunks) == 2
        assert chunks[0]["content"] == "he"
        assert chunks[1]["content"] == "llo"
