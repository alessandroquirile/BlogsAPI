from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.models.blog import Blog as BlogModel

client = TestClient(app)


# Test: Get all blogs
def test_get_all_blogs(db_session):
    response = client.get("/blogs")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "b1"


# Test: Get blog by ID
def test_get_blog_by_id(db_session):
    response = client.get("/blogs/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "b1"


# Test: create a blog (should raise error if not authorized)
def test_create_blog_unauthorized(db_session):
    response = client.post(
        "/blogs/create-blog",
        json={
            "title": "title",
            "description": "description",
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


# Test: create a blog (for an authenticated user)
def test_create_blog_authorized(db_session):
    response_login = client.post(
        "/login",
        data={
            "username": "u1",  # Usa un username valido per il test
            "password": "password1",  # Inserisci la password corretta
        },
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response_login.status_code == 200, response_login.text
    access_token = response_login.json().get("access_token")
    assert access_token, response_login.text

    response_create_blog = client.post(
        "/blogs/create-blog",
        json={
            "title": "title",
            "description": "description"
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    assert response_create_blog.status_code == 201, response_create_blog.text
    assert response_create_blog.json()["title"] == "title"
    assert response_create_blog.json()["description"] == "description"


# Test: Un utente non autenticato non può fare PUT, DELETE e POST
def test_unauthorized_user_cannot_modify_blogs(db_session):
    # Tentativo di aggiornamento (PUT) senza autenticazione
    response_put = client.put(
        "/blogs/1",
        json={"title": "new title", "description": "new description"}
    )
    assert response_put.status_code == status.HTTP_401_UNAUTHORIZED, response_put.text

    # Tentativo di eliminazione (DELETE) senza autenticazione
    response_delete = client.delete("/blogs/1")
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED, response_delete.text


# Funzione di login per ottenere il token di accesso
def login_user(username, password):
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert response.status_code == 200, response.text
    return response.json().get("access_token")


# Test: Un utente autenticato può modificare solo il proprio blog
def test_authenticated_user_can_modify_own_blog(db_session):
    # Login dell'utente u1
    access_token = login_user("u1", "password1")

    # Tentativo di aggiornare il proprio blog
    response_put = client.put(
        "/blogs/1",
        json={"title": "Updated title", "description": "Updated description"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response_put.status_code == status.HTTP_202_ACCEPTED, response_put.text


# Test: Un admin può eliminare il blog di qualsiasi utente
def test_admin_can_delete_any_blog(db_session):
    # Login dell'admin (u2)
    admin_token = login_user("u2", "password2")

    # Creazione di un blog di un utente normale (u1)
    db_session.add(BlogModel(title="User blog", description="User content", user_id=1))
    db_session.commit()

    # Tentativo dell'admin di eliminare il blog dell'utente (ID 1)
    response_delete = client.delete("/blogs/1", headers={"Authorization": f"Bearer {admin_token}"})
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT, response_delete.text
