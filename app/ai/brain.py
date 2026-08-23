from app.ai.intent import detect_intent

from app.tools.applications import open_application
from app.tools.system import get_system_information, get_time
from app.tools.files import list_downloads


def process_command(command: str):

    intent = detect_intent(command)

    if intent.name == "open_application":

        return open_application(
            intent.target
        )

    if intent.name == "system_information":

        return get_system_information()

    if intent.name == "get_time":

        return {
            "time": get_time()
        }

    if intent.name == "list_downloads":

        return {
            "downloads": list_downloads()
        }

    return {
        "message": "I don't understand that command yet.",
        "intent": intent.name
    }