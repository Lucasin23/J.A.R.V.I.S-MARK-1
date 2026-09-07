"""Entry point for J.A.R.V.I.S MARK 1."""

from __future__ import annotations

import os

from core.brain import JarvisConfigurationError, load_environment, reset_conversation, think
from voice.listener import VoiceListener
from voice.speaker import speak
from voice.wake_word import command_after_wake_word


load_environment()
WAKE_WORD = os.getenv("JARVIS_WAKE_WORD", "jarvis")
SHUTDOWN_COMMANDS = {"exit", "quit", "shutdown", "shut down", "goodbye"}


def reply(text: str) -> None:
    print(f"JARVIS: {text}")
    speak(text)


def main():
    print("J.A.R.V.I.S MARK I ONLINE.")
    print(f"Systems initialized. Say 'Hey {WAKE_WORD.title()}' to begin.\n")

    listener = VoiceListener()
    reply("JARVIS Mark One online.")

    while True:
        transcript = listener.listen()
        command = command_after_wake_word(transcript, WAKE_WORD)

        # Ignore ordinary conversation until the wake word is heard.
        if command is None:
            continue

        # Support both "Hey Jarvis, tell me a joke" and "Hey Jarvis" then a command.
        if not command:
            reply("Yes?")
            command = listener.listen(timeout=7, phrase_time_limit=12)
            if not command:
                continue

        normalised_command = command.lower().strip()
        if normalised_command in SHUTDOWN_COMMANDS:
            reply("Shutting down. Goodbye.")
            return

        if normalised_command in {"reset conversation", "clear conversation"}:
            reset_conversation()
            reply("Conversation reset. Your saved memories are still intact.")
            continue

        try:
            response = think(command)
        except JarvisConfigurationError as error:
            response = str(error)
        reply(response)


if __name__ == "__main__":
    main()
