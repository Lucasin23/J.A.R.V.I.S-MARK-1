"""Safe, local skills for everyday JARVIS use on macOS."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTES_FILE = PROJECT_ROOT / "data" / "notes.json"

# These aliases are intentionally limited. JARVIS does not run shell commands.
APP_ALIASES = {
    "calendar": "Calendar",
    "chrome": "Google Chrome",
    "code": "Visual Studio Code",
    "finder": "Finder",
    "notes": "Notes",
    "safari": "Safari",
    "spotify": "Spotify",
    "visual studio code": "Visual Studio Code",
}


class LocalSkills:
    """Handles private notes and a small, explicit set of app-launch requests."""

    def __init__(
        self,
        notes_file: Path = DEFAULT_NOTES_FILE,
        app_launcher: Callable[[str], None] | None = None,
    ) -> None:
        self.notes_file = notes_file
        self.app_launcher = app_launcher or self._open_macos_application

    def handle(self, command: str) -> str | None:
        """Return a local response when a known skill matches the command."""
        stripped = command.strip()
        normalised = stripped.lower().rstrip("?.!")

        if normalised.startswith("open "):
            return self._open_application(normalised[len("open ") :].strip())

        for prefix in ("take note ", "make a note ", "note that "):
            if normalised.startswith(prefix):
                return self._add_note(stripped[len(prefix) :].strip())

        if normalised in {"read my notes", "read notes", "what are my notes"}:
            return self._read_notes()

        return None

    def _open_application(self, requested_app: str) -> str:
        application = APP_ALIASES.get(requested_app)
        if not application:
            available = ", ".join(APP_ALIASES[name] for name in sorted(APP_ALIASES) if name != "code")
            return f"I can safely open: {available}."

        try:
            self.app_launcher(application)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return f"I couldn't open {application}."
        return f"Opening {application}."

    @staticmethod
    def _open_macos_application(application: str) -> None:
        subprocess.run(
            ["open", "-a", application],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _load_notes(self) -> list[dict[str, str]]:
        if not self.notes_file.exists():
            return []
        try:
            data = json.loads(self.notes_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return data if isinstance(data, list) else []

    def _save_notes(self, notes: list[dict[str, str]]) -> None:
        self.notes_file.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = self.notes_file.with_suffix(".tmp")
        temporary_file.write_text(json.dumps(notes, indent=2), encoding="utf-8")
        temporary_file.replace(self.notes_file)

    def _add_note(self, text: str) -> str:
        if not text:
            return "Tell me what you would like me to note."
        notes = self._load_notes()
        notes.append({"text": text, "created_at": datetime.now().isoformat(timespec="seconds")})
        self._save_notes(notes)
        return "Noted."

    def _read_notes(self) -> str:
        notes = self._load_notes()
        if not notes:
            return "You don't have any saved notes."
        recent_notes = [note.get("text", "") for note in notes[-5:] if note.get("text")]
        return "Your latest notes are: " + "; ".join(recent_notes) + "."
