from http import HTTPStatus

from fast_api.schemas import UserPublicSchema
from tests.conftest import other_user


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "teste",
            "email": "test@test.com",
            "password": "teste",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "teste",
        "email": "test@test.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": user.id,
    }


# def test_update_integrity_error(client, user, token):
#     # Inserindo fausto
#     client.post(
#         "/users",
#         json={
#             "username": "fausto",
#             "email": "fausto@example.com",
#             "password": "secret",
#         },
#     )

#     # Alterando o user das fixture para fausto
#     response_update = client.put(
#         f"/users/{user.id}",
#         headers={"Authorization": f"Bearer {token}"},
#         json={
#             "username": "fausto2",
#             "email": "bob@example.com",
#             "password": "mynewpassword",
#         },
#     )

#     assert response_update.status_code == HTTPStatus.CONFLICT
#     assert response_update.json() == {"detail": "Username or Email already exists"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_token_inexistent_user(client):
    response = client.post(
        "/auth/token",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "incorrect username or password"}
