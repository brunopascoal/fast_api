from http import HTTPStatus


def test_root_must_be_ok_and_return_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}
