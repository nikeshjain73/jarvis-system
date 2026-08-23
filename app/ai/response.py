def create_response(result: dict) -> str:

    if not result.get("success"):
        return result.get(
            "message",
            "Something went wrong."
        )

    intent = result.get("intent")

    if intent == "open_application":
        return result["result"]

    if intent == "get_time":
        return f"The current time is {result['result']['time']}."

    if intent == "system_information":
        system = result["result"]

        return (
            f"You are running {system['operating_system']} "
            f"{system['release']} on {system['machine']}."
        )

    if intent == "list_downloads":
        files = result["result"]["downloads"]

        return f"I found {len(files)} items in your Downloads folder."

    return "Command completed."