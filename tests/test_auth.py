def test_login_returns_token(client):
    response = client.post(
        "/auth/login",
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
        "/auth/login",
        json={
            "email": "user_c@example.com",
            "password": "password"
        } 
    )
    print(response.json())
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid Credentials"

def test_unknown_user_returns_401(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "user_c@e",
            "password": "password_c"
        } 
    )
    print(response.json())
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid Credentials"

def test_login_with_missing_password_returns_400(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "user_c@example.com",
            "password": ""
        } 
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json()["error"] == "Missing Credentials"