import speech_recognition as sr


recognizer = sr.Recognizer()
calibrated = False


def listen():
    global calibrated

    with sr.Microphone() as source:

        if not calibrated:
            print("JARVIS: Calibrating microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            calibrated = True
            print("JARVIS: Ready.")

        print("JARVIS: Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=1,
                phrase_time_limit=5
            )

        except sr.WaitTimeoutError:
            return ""

        try:
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text

        except sr.UnknownValueError:
            print("JARVIS: I didn't understand that.")
            return ""

        except sr.RequestError as error:
            print(f"JARVIS: Speech recognition error: {error}")
            return ""