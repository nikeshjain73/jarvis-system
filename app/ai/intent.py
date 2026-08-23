from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Intent:

    name: str
    target: Optional[str] = None
    parameters: Optional[dict] = None


def clean_command(command: str) -> str:

    command = command.lower().strip()

    # Remove common polite phrases
    prefixes = [
        "please ",
        "could you ",
        "can you ",
        "would you ",
        "will you ",
        "jarvis ",
    ]

    for prefix in prefixes:

        if command.startswith(prefix):
            command = command[len(prefix):].strip()

    # Remove trailing polite words
    command = re.sub(
        r"\s+(please|thanks|thank you)$",
        "",
        command
    )

    return command.strip()


def detect_intent(command: str) -> Intent:

    command = clean_command(command)

    # --------------------------------
    # OPEN
    # --------------------------------

    for prefix in [
        "open ",
        "launch ",
        "start ",
        "run "
    ]:

        if command.startswith(prefix):

            target = command[len(prefix):].strip()

            if not target:
                return Intent("unknown")

            return Intent(
                name="open_application",
                target=target
            )

    # --------------------------------
    # CLOSE
    # --------------------------------

    for prefix in [
        "close ",
        "exit ",
        "quit ",
        "stop "
    ]:

        if command.startswith(prefix):

            target = command[len(prefix):].strip()

            if not target:
                return Intent("unknown")

            return Intent(
                name="close_application",
                target=target
            )

    # --------------------------------
    # CHECK RUNNING
    # --------------------------------

    patterns = [
        r"^is (.+) running$",
        r"^is (.+) open$",
        r"^check (.+)$"
    ]

    for pattern in patterns:

        match = re.match(pattern, command)

        if match:

            return Intent(
                name="check_application",
                target=match.group(1).strip()
            )

    # --------------------------------
    # RUNNING APPLICATIONS
    # --------------------------------

    if (
        "what applications are running" in command
        or "which applications are running" in command
        or "what apps are running" in command
        or "which apps are running" in command
        or "what apps are open" in command
        or command == "running applications"
    ):

        return Intent(
            name="running_applications"
        )

    # --------------------------------
    # SYSTEM
    # --------------------------------

    if (
        "system information" in command
        or "system info" in command
        or command == "system"
    ):

        return Intent(
            name="system_information"
        )

    # --------------------------------
    # TIME
    # --------------------------------

    if (
        "what time" in command
        or "current time" in command
        or command == "time"
    ):

        return Intent(
            name="get_time"
        )

    # --------------------------------
    # DOWNLOADS
    # --------------------------------

    if (
        "list downloads" in command
        or "show downloads" in command
        or "my downloads" in command
    ):

        return Intent(
            name="list_downloads"
        )

    return Intent(
        name="unknown"
    )