"""Microphone input and speech-to-text for JARVIS."""

from __future__ import annotations

import speech_recognition as sr


class VoiceListener:
    """Listens one phrase at a time, calibrating the microphone only once."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.calibrated = False

    def listen(self, timeout: int = 4, phrase_time_limit: int = 8) -> str:
        """Return a transcript, or an empty string when no clear speech is heard."""
        try:
            with sr.Microphone() as source:
                if not self.calibrated:
                    print("JARVIS: Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    self.calibrated = True
                    print("JARVIS: Ready. Say 'Hey Jarvis' when you need me.")

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
        except sr.WaitTimeoutError:
            return ""
        except OSError as error:
            print(f"JARVIS: I cannot access the microphone: {error}")
            return ""

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as error:
            print(f"JARVIS: Speech recognition is unavailable: {error}")
            return ""
