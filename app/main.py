# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from datetime import datetime

from app.api.commands import router as command_router
from app.api.devices import router as device_router


app = FastAPI(
    title="JARVIS Ecosystem",
    description="Personal AI and Device Ecosystem",
    version="0.2.1"
)


app.include_router(command_router)
app.include_router(device_router)


@app.get("/")
def root():

    return {
        "name": "JARVIS",
        "system": "JARVIS Ecosystem",
        "version": "0.2.1",
        "status": "online"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }