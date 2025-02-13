from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.settings import Settings

settings = Settings()

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# gerenate a hash for a password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# verify the password, comparing the original password with the hash generated
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    # added a time for 30 minutes expire
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # add the time expire to dict to_encode using method update
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_username = payload.get('sub')

        if not subject_username:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.username == subject_username)
    )

    if not user:
        raise credentials_exception

    return user