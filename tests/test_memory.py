import tempfile
import unittest
from pathlib import Path

import memory.memory as memory


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.original_memory_file = memory.MEMORY_FILE
        memory.MEMORY_FILE = Path(self.temp_directory.name) / "memory.json"

    def tearDown(self):
        memory.MEMORY_FILE = self.original_memory_file
        self.temp_directory.cleanup()

    def test_remember_recall_and_forget(self):
        memory.remember("favourite colour", "blue")
        self.assertEqual(memory.recall("favourite colour"), "blue")
        self.assertEqual(memory.memory_keys(), ["favourite colour"])
        self.assertTrue(memory.forget("favourite colour"))
        self.assertIsNone(memory.recall("favourite colour"))

    def test_forget_reports_missing_memory(self):
        self.assertFalse(memory.forget("missing"))
