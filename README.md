# 📌 FastAPI TODO API

This is a **FastAPI** project that provides a **TODO management system** with **JWT-based authentication**. It utilizes **SQLAlchemy ORM** for database interactions and **Alembic** for migrations.

## 🚀 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [JWT](https://jwt.io/)
- [SQLite/](https://www.sqlite.org/)
- [Pytest](https://pytest.org/)

---

## 🛠️ Project Setup

### 🔹 Prerequisites

- Python **3.13+**
- Virtual environment manager (**Poetry**, **Pipenv**, or `venv`)
- A compatible database (e.g., **SQLite, PostgreSQL, MySQL**)

### 🔹 Installation

#### 1️⃣ Clone the repository

```sh
git clone https://github.com/brunopascoal/fast_api
cd fast_api
```

#### 2️⃣ Create and activate a virtual environment

Using venv

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

#### 4️⃣ Set up environment variables

Create a `.env` file and add the following:

```ini
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
````

#### 5️⃣ Run database migrations

```
alembic upgrade head
```

#### 6️⃣ Start the server with uvicorn (Recommended)

```
uvicorn fast_api.main:app --reload
```

## 🔐 Authentication

The API uses **JWT** for authentication. To access protected routes, you need to obtain an access token.

### 📌 How to obtain a token?

Make a **POST** request to `/auth/token` with your credentials:

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=your_username&password=your_password'
```

### 🔹 Response

```json
{
  "access_token": "your_jwt_token",
  "token_type": "Bearer"
}
```

### 🔹 Using the token

Use this token to access protected routes by adding it to the request header:

```sh
Authorization: Bearer your_jwt_token
````

## 📌 API Routes

### 🧑‍💻 Authentication (`/auth`)

| Method | Route                  | Description                |
|--------|------------------------|----------------------------|
| `POST` | `/auth/token`          | Obtains a JWT token        |
| `POST` | `/auth/refresh_token`  | Refreshes a JWT token      |

---

### 📌 Users (`/users`)

| Method  | Route              | Description               |
|---------|--------------------|---------------------------|
| `POST`  | `/users/`          | Creates a new user        |
| `GET`   | `/users/`          | Lists all users          |
| `GET`   | `/users/{user_id}` | Gets a user by ID        |
| `PUT`   | `/users/{user_id}` | Updates a user           |
| `DELETE`| `/users/{user_id}` | Deletes a user           |

---

### ✅ Tasks (`/todos`)

| Method  | Route              | Description                  |
|---------|--------------------|------------------------------|
| `POST`  | `/todos/`          | Creates a new task          |
| `GET`   | `/todos/`          | Lists all user tasks        |
| `PATCH` | `/todos/{todo_id}` | Updates a task              |
| `DELETE`| `/todos/{todo_id}` | Deletes a task              |

## 🧪 Tests

The API includes automated tests for:

✅ Database connection  
✅ User authentication  
✅ User CRUD operations  
✅ Task CRUD operations  

To run the tests, use the following command:

```sh
pytest tests/
````

## 🏆 Contribution

Feel free to contribute! To do so, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature:

   ```sh
   git checkout -b my-feature
   ```

3. Create a new branch for your feature:

    ```sh
    git commit -m "My new feature"
    ```

4. Push to your branch:

    ```sh
    git push origin my-feature
    ```

5. Open a Pull Request.

## 📄 License

This project is licensed under the GNU GENERAL PUBLIC License. See the LICENSE file for more details.
