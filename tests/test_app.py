from fastapi.testclient import TestClient
from fast_api.app import app
from http import HTTPStatus

def test_read_root_ok_ola_mundo():
    client = TestClient(app) #arrange(organizar)
    response =client.get('/') #act(agir)
    assert response.status_code == HTTPStatus.OK #assert(afirmar)
    assert response.json() == {"message": "Hello World"} #assert(afirmar)