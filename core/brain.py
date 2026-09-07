"""Gemini-backed conversation brain for J.A.R.V.I.S MARK 1."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from memory.memory import recall, remember


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.7-flash"

SYSTEM_INSTRUCTION = """
You are JARVIS MARK 1, a personal AI assistant.

Be calm, intelligent, helpful, and confident.
Speak naturally like a real personal assistant.
Keep simple answers concise.
Never claim you performed an action unless you actually did it.
"""

_client: Any | None = None
_previous_interaction_id: str | None = None


class JarvisConfigurationError(RuntimeError):
    """Raised when local JARVIS setup is incomplete."""


def load_environment() -> None:
    """Load simple KEY=value pairs from the project's private .env file."""
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _get_client() -> Any:
    global _client
    if _client is not None:
        return _client

    load_environment()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "replace-with-your-key":
        raise JarvisConfigurationError(
            "Gemini is not configured. Create a private .env file from .env.example "
            "and add your GEMINI_API_KEY."
        )

    try:
        from google import genai
    except ImportError as error:
        raise JarvisConfigurationError(
            "The Gemini package is missing. Run: python3 -m pip install -r requirements.txt"
        ) from error

    _client = genai.Client(api_key=api_key)
    return _client


def reset_conversation() -> None:
    """Forget the current cloud conversation while keeping local saved memories."""
    global _previous_interaction_id
    _previous_interaction_id = None


def think(command: str) -> str:
    """Handle local memory commands or ask Gemini for a spoken answer."""
    global _previous_interaction_id
    command = command.strip()
    if not command:
        return "I'm listening."

    if command.lower().startswith("remember "):
        text = command[9:]

        if " is " in text:
            key, value = text.split(" is ", 1)
            remember(key.strip(), value.strip())
            return f"I'll remember that {key.strip()} is {value.strip()}."

        return "Say it like: remember my favourite colour is blue."

    if command.lower().startswith("what do you remember about "):
        key = command[27:].strip()
        value = recall(key)

        if value:
            return f"I remember that {key} is {value}."

        return f"I don't have anything saved about {key}."

    client = _get_client()
    options: dict[str, Any] = {
        "model": os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        "input": command,
        "system_instruction": SYSTEM_INSTRUCTION,
    }
    if _previous_interaction_id:
        options["previous_interaction_id"] = _previous_interaction_id

    try:
        interaction = client.interactions.create(**options)
    except Exception:
        return (
            "I couldn't reach Gemini. Check your internet connection, API key, "
            "selected model, and Free Tier usage limits."
        )

    _previous_interaction_id = getattr(interaction, "id", None)
    response = (getattr(interaction, "output_text", "") or "").strip()
    return response or "I didn't receive a response from Gemini."
