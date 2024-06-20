import json
import os
import resend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from json import JSONDecodeError
from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from backend.Routes import doctors
from backend.database import connect
from fastapi.middleware.cors import CORSMiddleware

from backend.Schema.schema import UserInput, EmailData
from backend.api.gemini_data import gemini_response

from bson import json_util
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')
sengrid_api_key = os.getenv('SENDGRID_API_KEY')


class ObjectIdEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


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


class Location_specialization(BaseModel):
    Location: str
    Specialization: str


@app.get("/")
def read_root():
    return {"message": "Hello! Welcome to Medbuddy."}


@app.post("/gemini_data")
async def root(user_input: UserInput) -> str | dict:
    response = gemini_response(user_input.Text)
    try:
        response_dict = json.loads(response)
        return response_dict
    except JSONDecodeError:
        pass
    return response



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
        for doctor in matched_doctors:
            doctor['_id'] = str(doctor['_id'])
        matched_doctors_str = json.loads(json_util.dumps(matched_doctors))
        return matched_doctors_str  # Return the list of matched doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/book_appointment/{doctor_id}")
async def book_appointment(doctor_id: str):
    try:
        doctor_id = ObjectId(doctor_id)

        doctor = db.get_collection('doctors').find_one({"_id": doctor_id})
        if doctor:
            return json.loads(json_util.dumps(doctor))
        else:
            return {"message": "Doctor not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/send_email")
async def send_email(email_data: EmailData):
    message_doctor = Mail(
        from_email='yakashadav26@gmail.com',
        to_emails=email_data.doctorEmail,
        subject='Appointment Booked',
        html_content=f'<strong>Booked for {email_data.username} at {email_data.time} on {email_data.date}</strong>')
    message_user = Mail(
        from_email='yakashadav26@gmail.com',
        to_emails=email_data.userEmail,
        subject='Appointment Booked',
        html_content=f'<strong>Booked with {email_data.doctorName} on {email_data.date} at {email_data.time}</strong>')

    try:
        sg = SendGridAPIClient(sengrid_api_key)
        response = sg.send(message_doctor)
        sg = SendGridAPIClient(sengrid_api_key)
        response = sg.send(message_user)
        return {"message": "Appointment Booked and Confirmation has been sent to your email"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")


