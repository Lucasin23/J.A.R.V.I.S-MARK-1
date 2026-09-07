import subprocess
import os


def speak(text: str) -> None:
    """Speak a response with macOS's built-in voice, without blocking on errors."""
    if not text.strip():
        return

    rate = os.getenv("JARVIS_SPEECH_RATE", "185")
    command = ["say", "-r", rate]
    voice = os.getenv("JARVIS_VOICE")
    if voice:
        command.extend(["-v", voice])
    command.append(text)

    try:
        subprocess.run(command, check=False)
    except FileNotFoundError:
        # Keeping the printed response means the program also works off macOS.
        pass
