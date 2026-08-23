from app.voice.listener import VoiceListener
from app.voice.speaker import VoiceSpeaker

from app.ai.brain import process_command
from app.ai.response import create_response


class VoiceController:

    def __init__(self):

        self.listener = VoiceListener()
        self.speaker = VoiceSpeaker()

    def start(self):

        self.speaker.speak(
            "JARVIS voice system is online."
        )

        while True:

            try:

                command = self.listener.listen()

                if not command:
                    continue

                command_lower = command.lower().strip()

                if command_lower in [
                    "exit",
                    "quit",
                    "shutdown jarvis",
                    "stop listening"
                ]:

                    self.speaker.speak(
                        "Voice system shutting down."
                    )

                    break

                result = process_command(
                    command
                )

                response = create_response(
                    result
                )

                self.speaker.speak(
                    response
                )

            except KeyboardInterrupt:

                print("\nJARVIS stopped.")

                break

            except Exception as error:

                print(
                    f"Voice system error: {error}"
                )