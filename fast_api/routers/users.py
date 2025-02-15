from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from http import HTTPStatus
from fast_api.security import get_current_user, get_password_hash

from fast_api.schemas import UserSchema, UserPublicSchema, UserList, Message

from fast_api.database import get_session
from fast_api.models import User

router = APIRouter(prefix="/users", tags=["users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists"
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserList)
def read_users(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    user = session.scalars(select(User).limit(limit).offset(skip))

    return {"users": user}


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def read_users_by_id(user_id: int, session: T_Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return db_user


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permission")

    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Username or Email already exists"
        )


@router.delete("/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permission")

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted"}
