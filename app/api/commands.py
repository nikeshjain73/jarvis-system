from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.brain import process_command
from app.ai.response import create_response


router = APIRouter(
    prefix="/commands",
    tags=["Commands"]
)


class CommandRequest(BaseModel):

    command: str = Field(
        min_length=1,
        max_length=500
    )


@router.post("")
def execute_command(request: CommandRequest):

    result = process_command(
        request.command
    )

    response = create_response(result)

    return {
        "command": request.command,
        "success": result.get("success"),
        "intent": result.get("intent"),
        "response": response,
        "data": result
    }