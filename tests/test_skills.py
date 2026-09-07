import tempfile
import unittest
from pathlib import Path

from core.skills import LocalSkills


class LocalSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.opened_apps: list[str] = []
        self.skills = LocalSkills(
            notes_file=Path(self.temp_directory.name) / "notes.json",
            app_launcher=self.opened_apps.append,
        )

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_can_save_and_read_private_notes(self):
        self.assertEqual(self.skills.handle("take note buy oat milk"), "Noted.")
        self.assertEqual(self.skills.handle("read my notes"), "Your latest notes are: buy oat milk.")

    def test_only_known_apps_can_be_opened(self):
        self.assertEqual(self.skills.handle("open chrome"), "Opening Google Chrome.")
        self.assertEqual(self.opened_apps, ["Google Chrome"])
        self.assertIn("I can safely open", self.skills.handle("open terminal"))
        self.assertEqual(self.opened_apps, ["Google Chrome"])
