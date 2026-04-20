import asyncio
from core.services.stream_parser import StreamParser

async def test_parser():
    parser = StreamParser()
    
    async def mock_stream():
        chunks = [
            "Hello, ",
            "I will start thinking now. <|think|>",
            "This is a secret thought.",
            " I am reasoning about the universe.",
            "</|think|> Now I am back.",
            " Mission complete."
        ]
        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.1)

    print("Testing Stream Parser...")
    async for content, is_thinking in parser.parse(mock_stream()):
        type_str = "THOUGHT" if is_thinking else "CONTENT"
        print(f"[{type_str}]: {content}")

if __name__ == "__main__":
    asyncio.run(test_parser())
