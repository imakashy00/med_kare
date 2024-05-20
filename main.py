from fastapi import FastAPI, Depends
from backend.database import connect

from backend.Routes import gemini_route

app = FastAPI()
app.include_router(gemini_route.router)


@app.get("/doctors")
async def get_doctors(db: Depends(connect.mongodb)):
    doctors_collection = db["doctors"]  # Access the "doctors" collection
    doctors = await doctors_collection.find().to_list(length=100)  # Fetch a limited number of doctors
    return doctors
