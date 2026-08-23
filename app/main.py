from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

from app.ai.brain import process_command


app = FastAPI(
    title="JARVIS Ecosystem",
    description="Personal AI and Device Ecosystem",
    version="0.2.0"
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def root():

    return {
        "name": "JARVIS",
        "system": "JARVIS Ecosystem",
        "version": "0.2.0",
        "status": "online"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/command")
def command(request: CommandRequest):

    result = process_command(
        request.command
    )

    return {
        "command": request.command,
        "result": result
    }