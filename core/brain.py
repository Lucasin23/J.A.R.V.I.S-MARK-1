from google import genai
from memory.memory import remember, recall

client = genai.Client()

MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """
You are JARVIS MARK 1, a personal AI assistant.

Be calm, intelligent, helpful, and confident.
Speak naturally like a real personal assistant.
Keep simple answers concise.
Never claim you performed an action unless you actually did it.
"""


def think(command):
    if command.lower().startswith("remember "):
        text = command[9:]

        if " is " in text:
            key, value = text.split(" is ", 1)
            remember(key.strip(), value.strip())
            return f"I'll remember that {key.strip()} is {value.strip()}."

    if command.lower().startswith("what do you remember about "):
        key = command[27:].strip()
        value = recall(key)

        if value:
            return f"I remember that {key} is {value}."

        return f"I don't have anything saved about {key}."

    response = client.models.generate_content(
        model=MODEL,
        contents=command,
        config={
            "system_instruction": SYSTEM_INSTRUCTION
        }
    )

    return response.text