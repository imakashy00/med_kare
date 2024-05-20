from fastapi import APIRouter

from backend.api.gemini_data import gemini_response
from backend.Schema.schema import Doc
import json

router = APIRouter()


@router.post("/gemini_data")
async def root(user_input: Doc):
    response =gemini_response(user_input.Text)
    print(response)
    response_dict = json.loads(response)
    return response_dict
