import uuid
import bcrypt
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from demo_backend_svc.app import app
from demo_backend_svc.models.auth import User, Session
from demo_backend_svc.models.base import get_db


@pytest.fixture
def create_user(db_session):
    # Create a user with a hashed password
    password = "correct_password"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username="testuser", password_hash=hashed_password, full_name="Test User")
    session = db_session
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_successful_login(client, db_session, create_user):
    # Prepare login data with correct credentials
    login_data = {
        "username": "testuser",
        "password": "correct_password"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "session_token" in json_response

    # Verify that the session exists in the database
    session_token = json_response["session_token"]
    session_record = db_session.query(Session).filter(Session.session_token == session_token).first()
    assert session_record is not None
    # Check that expiration timestamp is approximately 7 days ahead
    expected_expiration = session_record.expiration_timestamp
    delta = expected_expiration - datetime.utcnow()
    assert delta.days >= 6


def test_failed_login_wrong_password(client, create_user):
    # Attempt login with wrong password
    login_data = {
        "username": "testuser",
        "password": "wrong_password"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Invalid username or password"


def test_failed_login_nonexistent_user(client):
    # Attempt login with a user that doesn't exist
    login_data = {
        "username": "nonexistent",
        "password": "any_password"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Invalid username or password"
