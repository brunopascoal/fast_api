from http import HTTPStatus
from tests.conftest import client

def test_create_user_ok(client):
    
    response = client.post("/users/", json={
        "name": "testeusername", 
        "email": "test@test.com", 
        "password": "password"
        })
    
    assert response.status_code == HTTPStatus.CREATED #voltou status correto?
    assert response.json() == {
        "name": "testeusername",
        "email": "test@test.com",
        "id": 1
    }

def test_read_users_ok(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [
        {
            "id": 1,
            "name": "testeusername",
            "email": "test@test.com"
        }
    ]}

def test_update_user_ok(client):
    response = client.put("/users/1", json={
        "name": "testeusername2",
        "email": "test@test.com",
        "password": "password",

        "id": 1
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "name": "testeusername2",
        "email": "test@test.com"
    }


def test_delete_user_ok(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully"}


def test_delete_user_not_found(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}

