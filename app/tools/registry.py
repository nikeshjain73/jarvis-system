from app.tools.applications import open_application
from app.tools.system import get_system_information, get_time
from app.tools.files import list_downloads


TOOLS = {
    "open_application": open_application,
    "system_information": get_system_information,
    "get_time": get_time,
    "list_downloads": list_downloads,
}


def get_tool(name: str):
    return TOOLS.get(name)


def get_available_tools():
    return list(TOOLS.keys())