from fast_api.models import User

from sqlalchemy import select


def teste_create_user(session):
    user = User(username="teste", password="teste", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    user_from_db = session.scalar(select(User).where(User.email == "test@test.com"))

    assert user_from_db.email == "test@test.com"
