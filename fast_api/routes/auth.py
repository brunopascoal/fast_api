from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select

from fast_api.database import get_session
from fast_api.schemas import Token
from fast_api.security import verify_password, create_access_token
from fast_api.models import User


router = APIRouter(prefix="/auth", tags=["auth"])
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
def login_for_acess_token(session: T_Session, form_data: T_OAuth2Form):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "Bearer"}
