from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from models import UserRegister, UserInDB, User, Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()
DB = "auth"


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: Request, response: Response, user: UserRegister = Body(...)):
    hashed_password = request.app.password_hasher.hash_password(user.password)
    user_hashed = {"_id": user.username, "hashed_password": hashed_password}
    # insert user into database if not already exists
    if request.app.database[DB].find_one({"_id": user.username}): 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    new_user = request.app.database[DB].insert_one(user_hashed)
   # return response code
    if new_user:
        response.status_code = status.HTTP_201_CREATED
        response.body = "User created"
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = "User not created"
    return response

@router.post("/login",response_model=Token)
async def login_for_access_token(request:Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = request.app.database[DB].find_one({"_id": form_data.username})
    if not user or not request.app.password_hasher.verify_password(form_data.password, user.get('hashed_password')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("user", user.get('_id'))
    access_token = request.app.token_manager.create_token(data={"sub": user.get('_id')})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify/{token}", response_model=TokenData, status_code=status.HTTP_200_OK)
async def verify_token(request: Request, token: str ):
        return request.app.token_manager.decode_token(token)
  
