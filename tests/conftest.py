import pytest

from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine

from fast_api.app import app
from fastapi.testclient import TestClient
from fast_api.database import get_session
from fast_api.models import User, table_registry
from fast_api.security import get_password_hash

@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = 'teste'
    user = User(username="testeusername", email="teste@test.com", password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password # Monkey Patch
    return user

@pytest.fixture()
def token(client, user):
    response = client.post('/token', data={'username': user.username, 'password': user.clean_password})
    
    return response.json()['access_token']
    