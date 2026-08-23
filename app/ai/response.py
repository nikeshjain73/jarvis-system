def create_response(result: dict) -> str:

    if not result.get("success"):

        return result.get(
            "message",
            "Something went wrong."
        )

    intent = result.get("intent")

    if intent == "open_application":

        return result.get(
            "message",
            "Application opened."
        )

    if intent == "close_application":

        return result.get(
            "message",
            "Application closed."
        )

    if intent == "check_application":

        if result.get("result") is True:
            return "Yes, that application is currently running."

        return "No, that application is not currently running."

    if intent == "running_applications":

        applications = result.get(
            "result",
            []
        )

        return (
            f"There are {len(applications)} "
            "running processes."
        )

    if intent == "get_time":

        return (
            f"The current time is "
            f"{result['result']['time']}."
        )

    if intent == "system_information":

        system = result["result"]

        return (
            f"You are running "
            f"{system['operating_system']} "
            f"{system['release']}."
        )

    if intent == "list_downloads":

        files = result["result"]["downloads"]

        return (
            f"I found {len(files)} "
            "items in your Downloads folder."
        )

    return "Command completed."