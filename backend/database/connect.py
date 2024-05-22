from pymongo.mongo_client import MongoClient
from fastapi import FastAPI

app = FastAPI()

uri = "mongodb+srv://yakashadav26:dXFFU8fDOz0zzmw6@flashx.cs8nxkx.mongodb.net/?retryWrites=true&w=majority&appName=medbuddy"


def database(database_name):
    client = MongoClient(uri)
    return client[database_name]

