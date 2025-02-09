from http import HTTPStatus

from fastapi import FastAPI
from .schemas import Message
from fast_api.routes import users, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello World"}
