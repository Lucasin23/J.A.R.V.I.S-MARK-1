# J.A.R.V.I.S MARK 1

A local voice assistant powered by the Gemini API. Say **“Hey Jarvis”** followed by a request, or say **“Hey Jarvis”** and wait for its prompt.

## Setup

1. In [Google AI Studio](https://aistudio.google.com/), create a Gemini API key on the Free Tier.
2. In this folder, copy `.env.example` to a new file named `.env`.
3. Replace `replace-with-your-key` in `.env` with the key. Keep that file private; Git ignores it.
4. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. Start JARVIS:

   ```bash
   python3 main.py
   ```

   To test the conversation without the microphone, use:

   ```bash
   python3 main.py --text
   ```

## Commands

- “Hey Jarvis, what can you do?”
- “Hey Jarvis, remember my favourite colour is blue.”
- “Hey Jarvis, what do you remember about my favourite colour?”
- “Hey Jarvis, forget my favourite colour.”
- “Hey Jarvis, what time is it?”
- “Hey Jarvis, status.”
- “Hey Jarvis, reset conversation.”
- “Hey Jarvis, shutdown.”

The Gemini Free Tier has model and rate limits. This project uses Gemini's server-side conversation feature for natural multi-turn chat; free-tier API content may be used by Google to improve its products. Do not use it for private or sensitive information.
