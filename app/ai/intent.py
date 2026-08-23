
from dataclasses import dataclass
from typing import Optional


@dataclass
class Intent:
    name: str
    target: Optional[str] = None
    parameters: Optional[dict] = None


def detect_intent(command: str) -> Intent:
    command = command.lower().strip()

    # Open application
    if command.startswith("open "):
        target = command.replace("open ", "", 1).strip()

        return Intent(
            name="open_application",
            target=target
        )

    # System information
    if "system information" in command:
        return Intent(
            name="system_information"
        )

    if "system info" in command:
        return Intent(
            name="system_information"
        )

    # Current time
    if "what time" in command or command == "time":
        return Intent(
            name="get_time"
        )

    # List downloads
    if "list downloads" in command:
        return Intent(
            name="list_downloads"
        )

    return Intent(
        name="unknown"
    )