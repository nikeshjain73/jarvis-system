import platform
from datetime import datetime


def get_system_information():

    return {
        "operating_system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def get_time():

    now = datetime.now()

    return now.strftime("%I:%M %p")