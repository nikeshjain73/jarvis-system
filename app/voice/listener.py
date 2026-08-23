import speech_recognition as sr


class VoiceListener:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("\n🎤 Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        try:

            print("🧠 Understanding...")

            text = self.recognizer.recognize_google(
                audio
            )

            print(f"👤 You: {text}")

            return text

        except sr.UnknownValueError:

            print("❌ I couldn't understand that.")

            return None

        except sr.RequestError:

            print("❌ Speech recognition service unavailable.")

            return None