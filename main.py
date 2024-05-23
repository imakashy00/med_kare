import json
from json import JSONDecodeError

from bson import json_util
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.Routes import doctors
from backend.database import connect
from fastapi.middleware.cors import CORSMiddleware

from backend.Schema.schema import UserInput
from backend.api.gemini_data import gemini_response

app = FastAPI()
app.include_router(doctors.router)

db = connect.database("medbuddy")

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
async def root(user_input: UserInput) -> str | dict:
    response = gemini_response(user_input.Text)
    try:
        response_dict = json.loads(response)
        return response_dict
    except JSONDecodeError:
        pass
    return response

class Location_specialization(BaseModel):
    Location: str
    Specialization: str


@app.post("/match_doctor")
async def match_doctor(details: Location_specialization):
    try:
        print(details)
        doctors_list = db.get_collection('doctors').find({
            "Address.City": details.Location,  # Use a dictionary for filter criteria
            "Specialization": details.Specialization,
        })
        print("search done!")
        matched_doctors = list(doctors_list)  # Convert cursor to a list of matched doctors
        print(matched_doctors)
        if not matched_doctors:
            return []  # Return an empty list if no doctors are found
        matched_doctors_str = json.loads(json_util.dumps(matched_doctors))
        return matched_doctors_str  # Return the list of matched doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
