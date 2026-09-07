import unittest

from core.brain import think


class LocalCommandTests(unittest.TestCase):
    def test_help_does_not_need_gemini(self):
        self.assertIn("Gemini conversation", think("help"))

    def test_time_does_not_need_gemini(self):
        self.assertTrue(think("what time is it").startswith("It is "))
