from fastapi import APIRouter
from pydantic import BaseModel

from app.devices.manager import (
    register_device,
    get_devices
)


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


class DeviceRequest(BaseModel):

    device_id: str
    device_name: str
    device_type: str


@router.post("/register")
def register(request: DeviceRequest):

    device = register_device(
        request.device_id,
        request.device_name,
        request.device_type
    )

    return {
        "success": True,
        "device": device
    }


@router.get("")
def devices():

    return {
        "success": True,
        "devices": get_devices()
    }