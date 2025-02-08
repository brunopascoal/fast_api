from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from .schemas import UserSchema, UserPublicSchema, UserList, Message, Token
from fast_api.models import User
from fast_api.database import get_session
from fast_api.security import get_password_hash, verify_password, create_acess_token, get_current_user

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello World"}


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session=Depends(get_session)):
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


@app.get("/users", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit: int = 10, 
               skip: int = 0, 
               session=Depends(get_session),
               current_user = Depends(get_current_user)
               ):
    user = session.scalars(select(User).limit(limit).offset(skip))

    return {"users": user}


@app.get("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def read_users_by_id(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return db_user


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session), current_user = Depends(get_current_user)
):
  
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permission')
        
    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session=Depends(get_session), current_user = Depends(get_current_user)
):
    
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permission')

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted"}


@app.post("/token", response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="incorrect username or password")

    access_token = create_acess_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "Bearer"}

