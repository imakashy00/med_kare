import json

from fastapi import FastAPI
from backend.Routes import gemini_route, doctors

from fastapi.middleware.cors import CORSMiddleware

from backend.Schema.schema import UserInput
from backend.api.gemini_data import gemini_response

app = FastAPI()
app.include_router(gemini_route.router)
app.include_router(doctors.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/gemini_data")
async def root(user_input: UserInput):
    response_value = gemini_response(user_input.Text)
    response_dict = json.loads(response_value)
    return response_dict



