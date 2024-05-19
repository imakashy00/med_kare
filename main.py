
from fastapi import FastAPI

from Routes import gemini_data

app = FastAPI()
app.include_router(gemini_data.router)






