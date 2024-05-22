import json
from json import JSONDecodeError

from fastapi import FastAPI
from backend.Routes import doctors

from fastapi.middleware.cors import CORSMiddleware

from backend.Schema.schema import UserInput
from backend.api.gemini_data import gemini_response

app = FastAPI()
app.include_router(doctors.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/gemini_data")
async def root(user_input: UserInput) -> str | list[dict]:
    response = gemini_response(user_input.Text)
    try:
        response_dict = json.loads(response)
        return response_dict
    except JSONDecodeError:
        pass
    return response
