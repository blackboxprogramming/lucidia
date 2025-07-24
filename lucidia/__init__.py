"""
Lucidia AI package.

This package implements a simple conversational agent with a short‑term
memory and basic sentiment awareness.  Lucidia aims to provide a more
empathetic interaction than typical chatbots by remembering past
exchanges and tailoring responses according to the emotional tone
detected in user input.  See the `README.md` for an overview of the
project philosophy and usage instructions.
"""

from .core import LucidiaAI

__all__ = ["LucidiaAI"]
__version__ = "0.1.0"
