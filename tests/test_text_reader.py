import pytest
from pathlib import Path
import tempfile
from phases.tokenizer.StreamReader import ChunkedTextReader as StreamReader
from tests.test_utils import create_test_file

def test_next_returns_chunks_until_complete():
    path = create_test_file("one two three four five six seven")
    reader = StreamReader(path, word_limit=3)

    has_more, chunk = reader.next()
    assert has_more is True
    assert chunk == "one two three"

    has_more, chunk = reader.next()
    assert has_more is True
    assert chunk == "four five six"

    has_more, chunk = reader.next()
    assert has_more is True
    assert chunk == "seven"

    has_more, chunk = reader.next()
    assert has_more is False
    assert chunk is None

def test_next_handles_exact_multiple():
    path = create_test_file("alpha beta gamma delta")
    reader = StreamReader(path, word_limit=2)

    chunks = []
    while True:
        has_more, chunk = reader.next()
        if not has_more:
            break
        chunks.append(chunk)

    assert chunks == ["alpha beta", "gamma delta"]

def test_next_handles_large_limit():
    path = create_test_file("a b c d e")
    reader = StreamReader (path, word_limit=50)

    has_more, chunk = reader.next()
    assert has_more is True
    assert chunk == "a b c d e"

    has_more, chunk = reader.next()
    assert has_more is False
    assert chunk is None
