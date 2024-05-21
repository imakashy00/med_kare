from fastapi import APIRouter, Response
from starlette.responses import JSONResponse
from backend.api.gemini_data import gemini_response
from backend.Schema.schema import UserInput
import json

router = APIRouter()


# @router.post("/gemini_data")
# async def root(user_input: UserInput):
#     response_value = gemini_response(user_input.Text)
#     response_dict = json.loads(response_value)
#     return response_dict
