from jwt import decode

from fast_api.security import create_acess_token, SECRET_KEY, ALGORITHM


def test_jwt():
    data = {"sub": "test@test.com"}
    token = create_acess_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result["sub"] == data["sub"]
    assert result["exp"]
