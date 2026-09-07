import unittest

from voice.wake_word import command_after_wake_word


class WakeWordTests(unittest.TestCase):
    def test_returns_command_after_hey_jarvis(self):
        self.assertEqual(
            command_after_wake_word("Hey Jarvis, tell me a joke"),
            "tell me a joke",
        )

    def test_allows_wake_word_without_a_command(self):
        self.assertEqual(command_after_wake_word("Jarvis"), "")

    def test_ignores_speech_without_the_wake_word(self):
        self.assertIsNone(command_after_wake_word("What time is it?"))


if __name__ == "__main__":
    unittest.main()
