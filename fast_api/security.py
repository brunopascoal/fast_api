from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from http import HTTPStatus
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy import select
from fast_api.database import get_session
from fast_api.models import User

pwd_context = PasswordHash.recommended()

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


# gerenate a hash for a password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# verify the password, comparing the original password with the hash generated
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data: dict):
    to_encode = data.copy()

    # added a time for 30 minutes expire
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    # add the time expire to dict to_encode using method update
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
def get_current_user(session = Depends(get_session), token = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, 
        detail='Could not validade credentials', 
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
        
    user_db = session.scalar(select(User).where(User.username == username))
    
    if not user_db:
        raise credentials_exception