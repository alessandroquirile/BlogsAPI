from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_login_username_not_found(db_session):
    username = "nonexistentusername"
    response = client.post(
        "/login",
        data={
            "username": f"{username}",  # Username not found in the database
            "password": "password",  # Any password
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"User id={username} not found"


def test_login_invalid_password(db_session):
    response = client.post(
        "/login",
        data={
            "username": "u1",  # Valid username
            "password": "wrongpassword",  # Incorrect password
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    print(response.headers)
    assert response.headers["WWW-Authenticate"] == "Bearer"
    data = response.json()
    assert data["detail"] == "Not authorized"


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
