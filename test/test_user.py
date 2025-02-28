import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.blog import Blog as BlogModel
from src.models.user import User as UserModel
from src.utils.database import Base, get_db
from src.utils.hashing import bcrypt

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSession()

    # Create some mock users
    user1 = UserModel(id=1, username="u1", email="email1", password=bcrypt("password1"), is_admin=False)
    user2 = UserModel(id=2, username="u2", email="email2", password=bcrypt("password2"), is_admin=True)
    blog1 = BlogModel(title="b1", description="d1", user_id=1)
    db.add(user1)
    db.add(user2)
    db.add(blog1)
    db.commit()

    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_user(db_session):
    response = client.post(
        "/users",
        json={
            "username": "username",
            "email": "test@test.com",
            "password": "password",
            "is_admin": False
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["username"] == "username"
    assert data["email"] == "test@test.com"
    assert data["is_admin"] == False


def test_get_user(db_session):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["username"] == "u1"
    assert data["email"] == "email1"
    assert data["is_admin"] == False
    assert len(data["blogs"]) == 1
    assert data["blogs"][0]["title"] == "b1"
    assert data["blogs"][0]["description"] == "d1"


def test_get_user_not_found(db_session):
    user_id = 9999
    response = client.get(f"/users/{user_id}")  # Non-existent user ID
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"User id={user_id} not found"


def test_get_all_users(db_session):
    response = client.get("/users")

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data) == 2

    # Verify the first user
    assert data[0]["username"] == "u1"
    assert data[0]["email"] == "email1"
    assert data[0]["is_admin"] == False
    assert len(data[0]["blogs"]) == 1  # The first user has 1 associated blog
    assert data[0]["blogs"][0]["title"] == "b1"
    assert data[0]["blogs"][0]["description"] == "d1"

    # Verify the second user
    assert data[1]["username"] == "u2"
    assert data[1]["email"] == "email2"
    assert data[1]["is_admin"] == True
    assert len(data[1]["blogs"]) == 0  # The second user has no blogs


def test_create_user_already_exists(db_session):
    # Try to create an user with the same username and email
    response = client.post(
        "/users",
        json={
            "username": "u1",  # Same username
            "email": "email1",  # Same email
            "password": "password",
            "is_admin": False
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "User already exists"


def test_login_username_not_found(db_session):
    response = client.post(
        "/login",
        data={
            "username": "nonexistentusername",  # Username not found in the database
            "password": "password",  # Any password
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "Username not found"


def test_login_invalid_password(db_session):
    response = client.post(
        "/login",
        data={
            "username": "u1",  # Valid username
            "password": "wrongpassword",  # Incorrect password
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    data = response.json()
    assert data["detail"] == "Invalid credentials"


def test_login_valid_credentials(db_session):
    response = client.post(
        "/login",
        data={
            "username": "u1",
            "password": "password1"
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert "access_token" in response.json()
    token = response.json()["access_token"]
    assert token is not None


def test_get_blog_not_found(db_session):
    blog_id = 9999  # Assume 9999 is a non-existent ID
    response = client.get(f"/blogs/{blog_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Blog id={blog_id} not found"
