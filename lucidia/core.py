"""Lucidia core — conversational AI agent with sentiment analysis and memory."""

import json
import os


class LucidiaAI:
    POSITIVE_WORDS = [
        "happy", "great", "wonderful", "excellent", "good", "love",
        "amazing", "fantastic", "beautiful", "excited", "joy", "pleased",
    ]
    NEGATIVE_WORDS = [
        "sad", "terrible", "awful", "bad", "hate", "horrible",
        "angry", "depressed", "miserable", "upset", "pain", "fear",
    ]

    def __init__(self, memory_file=None):
        self.memory = []
        self.memory_file = memory_file
        if memory_file and os.path.exists(memory_file):
            try:
                with open(memory_file, "r") as f:
                    self.memory = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.memory = []

    def analyze_sentiment(self, text: str) -> int:
        words = text.lower().split()
        pos = sum(1 for w in words if w in self.POSITIVE_WORDS)
        neg = sum(1 for w in words if w in self.NEGATIVE_WORDS)
        if pos > neg:
            return 1
        elif neg > pos:
            return -1
        return 0

    def generate_response(self, message: str) -> str:
        for entry in self.memory:
            if entry["user"] == message:
                response = f"You mentioned that before. {message}"
                self.add_to_memory(message, response)
                return response

        sentiment = self.analyze_sentiment(message)

        if self.memory:
            prev = self.memory[-1]["user"]
            if sentiment > 0:
                response = f"That's wonderful to hear! Earlier you talked about: {prev}"
            elif sentiment < 0:
                response = f"I'm sorry to hear that. Earlier you talked about: {prev}"
            else:
                response = f"I see how you feel about that. Earlier you talked about: {prev}"
        else:
            if sentiment > 0:
                response = "That's wonderful to hear!"
            elif sentiment < 0:
                response = "I'm sorry to hear that."
            else:
                response = "Tell me more about how you feel."

        self.add_to_memory(message, response)
        return response

    def add_to_memory(self, user_msg: str, lucidia_msg: str):
        self.memory.append({"user": user_msg, "lucidia": lucidia_msg})

    def save_memory(self, path=None):
        target = path or self.memory_file
        if not target:
            return
        with open(target, "w") as f:
            json.dump(self.memory, f)
