from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserInput(BaseModel):
    Text: Optional[str] = None


class Name(BaseModel):
    First: str
    Last: str


class Contact(BaseModel):
    Email: str
    Phone: str


class ImageMetaData(BaseModel):
    ImageName: str
    ImageSize: str


class TimeSlot(BaseModel):
    Day: str
    start: str
    end: str
    isAvailable: bool


class UserAppointment(BaseModel):
    patientId: str
    date: str


class LocationAdd(BaseModel):
    Address: str
    city: str
    state: str
    pincode: int


class DocRegister(BaseModel):
    Name: Name
    Contact: Contact
    Location: LocationAdd
    Specialization: str
    qualification: list[str]
    gender: Gender
    experience: int
    fee: int


class Doctor(DocRegister):
    id: Optional[str] = Field(alias="_id")
    timeSlots: Optional[list[TimeSlot]]


class User(BaseModel):
    Name: Name
    Contact: Contact
    Age: int
    Gender: Gender

