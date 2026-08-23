from app.ai.intent import detect_intent
from app.tools.registry import get_tool


def process_command(command: str):

    intent = detect_intent(command)

    if intent.name == "unknown":
        return {
            "success": False,
            "message": "I don't understand that command yet.",
            "intent": "unknown"
        }

    tool = get_tool(intent.name)

    if tool is None:
        return {
            "success": False,
            "message": f"Tool '{intent.name}' is not available.",
            "intent": intent.name
        }

    try:

        if intent.name == "open_application":

            result = tool(intent.target)

        else:

            result = tool()

        return {
            "success": True,
            "intent": intent.name,
            "result": result
        }

    except Exception as error:

        return {
            "success": False,
            "intent": intent.name,
            "error": str(error)
        }