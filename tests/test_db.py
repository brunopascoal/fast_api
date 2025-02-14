from fast_api.models import User

from sqlalchemy import select

from fast_api.models import Todo, User


def teste_create_user(session):
    user = User(username="teste", password="teste", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    user_from_db = session.scalar(select(User).where(User.email == "test@test.com"))

    assert user_from_db.email == "test@test.com"

# ...
def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos