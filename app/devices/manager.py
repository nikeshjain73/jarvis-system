from datetime import datetime


DEVICES = {}


def register_device(
    device_id: str,
    device_name: str,
    device_type: str
):

    device = {
        "device_id": device_id,
        "device_name": device_name,
        "device_type": device_type,
        "status": "online",
        "last_seen": datetime.now().isoformat()
    }

    DEVICES[device_id] = device

    return device


def get_devices():

    return list(DEVICES.values())


def get_device(device_id: str):

    return DEVICES.get(device_id)