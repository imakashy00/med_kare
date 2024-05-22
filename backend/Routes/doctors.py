from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from backend.Schema.schema import DocRegister
from backend.database import connect

router = APIRouter()
db = connect.database("medbuddy")


@router.post("/doctors")
async def add_doctor(doctor: DocRegister):
    doc = {
        "Name": {
            "First": doctor.Name.First,
            "Last": doctor.Name.Last
        },
        "Contact": {
            "Email": doctor.Contact.Email,
            "Phone": doctor.Contact.Phone
        },
        "Location": {
            "Address": doctor.Location.Address,
            "city": doctor.Location.city,
        },
        "Specialization": doctor.Specialization,
        "qualification": doctor.qualification,
        "rating": "4.5",
        "gender": doctor.gender,
        "experience": doctor.experience,
        "fee": doctor.fee,
        "TimeSlot": [],
    }
    try:
        db.get_collection('doctors').insert_one(doc)
        return {"message": "Doctor added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctors", response_model=List[DocRegister])
async def get_doctors():
    try:
        doctors = db.get_collection('doctors').find()
        print(doctors)
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
