from modules.thinking import ThinkingEngine


def test_thinking_detection():
    engine = ThinkingEngine()

    # Text before thinking
    chunk1 = "Hello, world! <|think|>This is a thought."
    clean, thought = engine.process_chunk(chunk1)

    assert clean == "Hello, world! "
    assert thought == "This is a thought."
    assert engine.is_thinking is True

    # Mid-thinking
    chunk2 = " Still thinking."
    clean, thought = engine.process_chunk(chunk2)
    assert clean == ""
    assert thought == " Still thinking."

    # End thinking
    chunk3 = " End.<|/think|> Here is the result."
    clean, thought = engine.process_chunk(chunk3)
    assert clean == " Here is the result."
    assert thought == " End."
    assert engine.is_thinking is False


def test_no_thinking():
    engine = ThinkingEngine()
    chunk = "Just a normal chunk without tags."
    clean, thought = engine.process_chunk(chunk)
    assert clean == chunk
    assert thought is None
    assert engine.is_thinking is False
