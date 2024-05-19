from fastapi import FastAPI, APIRouter
from api import gemini_data
from Schema import schema
import json

router = APIRouter()


@router.post("/gemini_data")
async def root(user_input: schema.Doc):
    response = gemini_data.gemini_response(user_input.Text)
    print(response)
    response_dict = json.loads(response)
    return response_dict
