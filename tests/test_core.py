"""Tests for lucidia.core — LucidiaAI conversational agent."""

import json
import os
import tempfile
import pytest

from lucidia.core import LucidiaAI


class TestSentimentAnalysis:
    def test_positive_sentiment(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("I am so happy today") == 1

    def test_negative_sentiment(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("I feel sad and awful") == -1

    def test_neutral_sentiment(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("The weather is cloudy") == 0

    def test_mixed_sentiment_positive_wins(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("happy great but sad") == 1

    def test_mixed_sentiment_tie_is_neutral(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("happy but sad") == 0

    def test_case_insensitive(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("I am HAPPY and EXCITED") == 1

    def test_empty_string_neutral(self):
        ai = LucidiaAI()
        assert ai.analyze_sentiment("") == 0

    def test_all_positive_words(self):
        ai = LucidiaAI()
        text = " ".join(LucidiaAI.POSITIVE_WORDS)
        assert ai.analyze_sentiment(text) == 1

    def test_all_negative_words(self):
        ai = LucidiaAI()
        text = " ".join(LucidiaAI.NEGATIVE_WORDS)
        assert ai.analyze_sentiment(text) == -1


class TestGenerateResponse:
    def test_positive_response(self):
        ai = LucidiaAI()
        resp = ai.generate_response("I had a great day!")
        assert "wonderful" in resp.lower()

    def test_negative_response(self):
        ai = LucidiaAI()
        resp = ai.generate_response("I feel terrible today")
        assert "sorry" in resp.lower()

    def test_neutral_response(self):
        ai = LucidiaAI()
        resp = ai.generate_response("The sky is blue")
        assert "feel" in resp.lower()

    def test_memory_callback(self):
        ai = LucidiaAI()
        ai.generate_response("First message")
        resp = ai.generate_response("Second message")
        assert "Earlier you talked about" in resp

    def test_repeated_message(self):
        ai = LucidiaAI()
        ai.generate_response("same thing")
        resp = ai.generate_response("same thing")
        assert "mentioned that before" in resp

    def test_adds_to_memory(self):
        ai = LucidiaAI()
        ai.generate_response("hello there")
        assert len(ai.memory) == 1
        assert ai.memory[0]["user"] == "hello there"


class TestMemory:
    def test_add_to_memory(self):
        ai = LucidiaAI()
        ai.add_to_memory("hi", "hello")
        assert len(ai.memory) == 1
        assert ai.memory[0] == {"user": "hi", "lucidia": "hello"}

    def test_save_and_load_memory(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            ai = LucidiaAI()
            ai.add_to_memory("test input", "test response")
            ai.save_memory(path)

            ai2 = LucidiaAI(memory_file=path)
            assert len(ai2.memory) == 1
            assert ai2.memory[0]["user"] == "test input"
        finally:
            os.unlink(path)

    def test_load_corrupt_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json{{{")
            path = f.name
        try:
            ai = LucidiaAI(memory_file=path)
            assert ai.memory == []
        finally:
            os.unlink(path)

    def test_save_no_file_does_nothing(self):
        ai = LucidiaAI()
        ai.add_to_memory("a", "b")
        ai.save_memory()  # no file set, should not raise

    def test_init_no_memory_file(self):
        ai = LucidiaAI()
        assert ai.memory == []
        assert ai.memory_file is None

    def test_init_nonexistent_file(self):
        ai = LucidiaAI(memory_file="/tmp/nonexistent_lucidia_test.json")
        assert ai.memory == []
