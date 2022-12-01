from typing import Union
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username:str 

class UserRegister(User):
    password: str

class UserInDB(BaseModel):
    username: str = Field(alias="_id")
    hashed_password: str
