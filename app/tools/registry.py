from app.tools.applications import open_application
from app.tools.system import get_system_information, get_time
from app.tools.files import list_downloads

from app.laptop.application_manager import ApplicationManager


application_manager = ApplicationManager()


TOOLS = {
    "open_application": application_manager.open_application,
    "close_application": application_manager.close_application,
    "check_application": application_manager.is_running,
    "running_applications": application_manager.get_running_applications,

    "system_information": get_system_information,
    "get_time": get_time,
    "list_downloads": list_downloads,
}


def get_tool(name: str):

    return TOOLS.get(name)


def get_available_tools():

    return list(TOOLS.keys())