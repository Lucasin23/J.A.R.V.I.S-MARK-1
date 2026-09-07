"""Wake-word matching that is easy to test and works with speech transcripts."""

from __future__ import annotations

import re


def command_after_wake_word(transcript: str, wake_word: str = "jarvis") -> str | None:
    """Return the words after the wake word, or ``None`` when it was not spoken."""
    cleaned_wake_word = " ".join(wake_word.lower().split())
    if not cleaned_wake_word:
        raise ValueError("A wake word is required.")

    pattern = re.compile(
        rf"\b(?:(?:hey|ok|okay)\s+)?{re.escape(cleaned_wake_word)}\b[\s,.:;!?-]*(.*)$",
        re.IGNORECASE,
    )
    match = pattern.search(transcript.strip())
    return match.group(1).strip() if match else None
