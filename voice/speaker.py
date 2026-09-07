import subprocess


def speak(text: str) -> None:
    """Speak a response with macOS's built-in voice, without blocking on errors."""
    if not text.strip():
        return

    try:
        subprocess.run(["say", "-r", "185", text], check=False)
    except FileNotFoundError:
        # Keeping the printed response means the program also works off macOS.
        pass
