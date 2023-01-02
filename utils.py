from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends,  HTTPException, status


from models import TokenData



class PasswordHasher():
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


class Token_Manager():
    def __init__(self, secret_key, algorithm, access_token_expire_minutes):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = int(access_token_expire_minutes)
    
    def create_token(self, data: dict):
        to_encode = data.copy()
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30*24*60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print(payload)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        return token_data
    







