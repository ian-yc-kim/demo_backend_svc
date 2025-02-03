from fastapi import status

def test_valid_signup(client):
    payload = {
        "username": "ValidUser_123",
        "password": "StrongP@ssw0rd",
        "full_name": "Valid User"
    }
    response = client.post("/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "user_id" in data
    assert data["username"] == payload["username"]


def test_duplicate_username(client):
    payload = {
        "username": "DuplicateUser",
        "password": "StrongP@ssw0rd",
        "full_name": "Duplicate User"
    }
    # First signup should succeed
    response1 = client.post("/signup", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED

    # Duplicate signup should fail
    response2 = client.post("/signup", json=payload)
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Username already exists"


def test_invalid_username(client):
    payload = {
        "username": "ab",
        "password": "StrongP@ssw0rd",
        "full_name": "Invalid Username"
    }
    response = client.post("/signup", json=payload)
    # Pydantic validation error returns a 422 status code
    assert response.status_code == 422


def test_weak_password(client):
    payload = {
        "username": "AnotherUser",
        "password": "weakpass",
        "full_name": "Weak Password"
    }
    response = client.post("/signup", json=payload)
    # Pydantic validation error returns a 422 status code
    assert response.status_code == 422
