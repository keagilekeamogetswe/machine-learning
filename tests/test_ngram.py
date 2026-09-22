import pytest
from phases.tokenizer.NGramExtractor import NgramExtractor

def test_ngram_stats_complex_word():
    tool = NgramExtractor("encyclopedia")
    stats = tool.getNgramStats()

    # Check some expected n-grams
    assert "ency" in stats
    assert stats["ency"]["size"] == 4
    assert stats["ency"]["frequency"] == 1

def test_ngram_stats_real_sentence():
    sentence = "The quick brown fox jumps over the lazy dog"
    tool = NgramExtractor(sentence)
    stats = tool.getNgramStats()

    # Check that common bigrams exist
    assert "Th" in stats
    assert "qu" in stats
    assert "do" in stats

    # Ensure frequency counts are correct for repeated words
    assert stats["he"]["frequency"] >= 2  # "The" and "the"

def test_ngram_stats_repeated_phrase():
    tool = NgramExtractor("data science data science")
    stats = tool.getNgramStats()

    # 'da' should appear multiple times
    assert "da" in stats
    assert stats["da"]["frequency"] == 2  # appears in both "data"

    # 'science' trigrams should exist
    assert "sci" in stats
    assert stats["sci"]["size"] == 3

def test_ngram_stats_mixed_case_and_punctuation():
    tool = NgramExtractor("AI-powered solutions, AI-powered future!")
    stats = tool.getNgramStats()

    # Check that punctuation doesn't break extraction
    assert "AI" in stats
    assert stats["AI"]["size"] == 2

    # 'pow' should exist from "powered"
    assert "pow" in stats
    assert stats["pow"]["frequency"] == 2
    # assert "AI-powered" in stats
    # assert stats["AI-powered"]["frequency"] == 2
