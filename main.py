from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI
from dotenv import dotenv_values
from routes import router

from utils import PasswordHasher, Token_Manager
from pymongo import MongoClient

from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()



origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"],
                # username=config["MONGO_INITDB_ROOT_USERNAME"],
                # password=config["MONGO_INITDB_ROOT_PASSWORD"],
                )
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    app.password_hasher = PasswordHasher()
    app.token_manager = Token_Manager(config.get("SECRET_KEY"), config.get("ALGORITHM"), config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    print("Created password hasher and token manager!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router, tags=[""], prefix="")


