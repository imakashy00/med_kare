from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId


class UserInput(BaseModel):
    Text: Optional[str] = None


class Contact(BaseModel):
    Email: str
    Phone: str


class ImageMetaData(BaseModel):
    ImageName: str
    ImageSize: str


class TimeSlot(BaseModel):
    Time: str
    isAvailable: bool


class Dateslots(BaseModel):
    Date: str
    TimeSlots: list[TimeSlot]


class Location(BaseModel):
    Street: str
    City: str


class DocRegister(BaseModel):
    Name: str
    Contact: Contact
    Address: Location
    Specialization: str
    Experience: str
    Fee: str


class Doctor(DocRegister):
    Rating: str
    TimeSlot: Optional[list[Dateslots]]


class EmailData(BaseModel):
    username: str
    userEmail: EmailStr
    doctorName: str
    doctorEmail: EmailStr
    date: str
    time: str
