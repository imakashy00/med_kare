from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from backend.Schema.schema import Doctor, DocRegister
from backend.database import connect

router = APIRouter()
db = connect.database("medbuddy")


@router.post("/doctors")
async def add_doctor(doctor: Doctor):

    try:
        db.get_collection('doctors').insert_one(doctor.dict())
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
