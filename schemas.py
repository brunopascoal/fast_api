from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserDB(UserSchema):
    id: int


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserList(BaseModel):
    users: list[UserPublicSchema]
