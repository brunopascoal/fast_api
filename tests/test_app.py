from http import HTTPStatus
from tests.conftest import client, user, token
from fast_api.schemas import UserPublicSchema


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED  # voltou status correto?
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": 1,
    }


def test_already_create_user(client):
    register = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "email": "test@test.com",
            "password": "password",
        },
    )

    response = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "email": "test@test.com",
            "password": "password",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST  # voltou status correto?


def test_read_users_with_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "username": "testeusername2",
            "email": "test@test.com",
            "password": "password",
            "id": 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testeusername2",
        "email": "test@test.com",
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_token(client, user):
    response = client.post('/token', data={'username': user.username, 'password': user.clean_password})
    
    token = response.json()
    
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token