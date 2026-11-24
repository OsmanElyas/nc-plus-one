from app.auth.password import verify_password
from app.db.queries.user import get_user
import pytest

def test_login_returns_token(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user_c@example.com",
            "password": "password_c"
        } 
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_with_wrong_password_returns_401(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user_c@example.com",
            "password": "password"
        } 
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid Credentials"

def test_unknown_user_returns_401(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user_c@e",
            "password": "password_c"
        } 
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid Credentials"

def test_login_with_missing_password_returns_400(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user_c@example.com",
            "password": ""
        } 
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Missing Credentials"


def test_creating_a_user_returns_201(client, db_cleanup):
    db_cleanup("DELETE FROM users WHERE email = %s", ("alice@exampleqe.com",))
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Alice Smith",
            "email": "alice@exampleqe.com",
            "password": "securepassword123"
            }
    )
    user = response.json()["user"]

    assert response.status_code == 201
    assert user["name"] == "Alice Smith"
    assert user["email"] == "alice@exampleqe.com"
    assert "password" not in user


def test_recreating_a_user_returns_409(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "user_c",
            "email": "user_c@example.com",
            "password": "securepassword123"
            }
    )

    assert response.status_code == 409
    assert response.json()["error"] == "Email already registered"


def test_registration_stores_hashed_password(client, db_cleanup):
    password = "securepassword123"
    email = "hash-check@example.com"
    db_cleanup("DELETE FROM users WHERE email = %s", (email,))

    response = client.post(
        "/api/auth/register",
        json={"name": "Hash Check", "email": email, "password": password},
    )

    stored_user = get_user(email)
    assert response.status_code == 201
    assert stored_user["password"] != password
    assert verify_password(password, stored_user["password"])
    assert "password" not in response.json()["user"]


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "missing-name@example.com", "password": "securepassword123"},
        {"name": "Missing Email", "password": "securepassword123"},
        {"name": "Missing Password", "email": "missing-password@example.com"},
    ],
)
def test_registration_with_missing_field_returns_400(client, payload):
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 400