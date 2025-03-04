from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


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
    username = "u1"
    response = client.post(
        "/users",
        json={
            "username": f"{username}",  # Same username
            "email": "email1",  # Same email
            "password": "password",
            "is_admin": False
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == f"User {username} already exists"


def test_get_blog_not_found(db_session):
    blog_id = 9999  # Assume 9999 is a non-existent ID
    response = client.get(f"/blogs/{blog_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Blog id={blog_id} not found"
