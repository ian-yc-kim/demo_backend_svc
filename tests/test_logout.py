import logging
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from demo_backend_svc.app import app
from demo_backend_svc.models.auth import Session as SessionModel

# Include the logout router for testing
from demo_backend_svc.routers.logout import router as logout_router
app.include_router(logout_router)


@pytest.fixture

def valid_session_token(db_session):
    """Fixture to create a valid session token record."""
    token = "valid-token-123"
    # Set expiration 10 minutes in the future
    expiration = datetime.utcnow() + timedelta(minutes=10)
    session_record = SessionModel(session_token=token, user_id='test-user', expiration_timestamp=expiration)
    db_session.add(session_record)
    db_session.commit()
    return token


@pytest.fixture

def expired_session_token(db_session):
    """Fixture to create an expired session token record."""
    token = "expired-token-123"
    # Set expiration 10 minutes in the past
    expiration = datetime.utcnow() - timedelta(minutes=10)
    session_record = SessionModel(session_token=token, user_id='test-user', expiration_timestamp=expiration)
    db_session.add(session_record)
    db_session.commit()
    return token


def test_valid_logout(client, db_session, valid_session_token):
    # Perform logout with valid session token
    response = client.post("/logout", headers={"Authorization": f"Bearer {valid_session_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Logout successful"
    # Verify that the session record has been removed
    session_in_db = db_session.query(SessionModel).filter(SessionModel.session_token == valid_session_token).first()
    assert session_in_db is None


def test_invalid_token_logout(client):
    # Use an invalid token
    response = client.post("/logout", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    data = response.json()
    assert "Invalid session token" in data.get("detail", "")


def test_missing_token_logout(client):
    # No Authorization header
    response = client.post("/logout")
    assert response.status_code == 401
    data = response.json()
    assert "Missing session token" in data.get("detail", "")


def test_expired_token_logout(client, db_session, expired_session_token):
    # Use an expired token
    response = client.post("/logout", headers={"Authorization": f"Bearer {expired_session_token}"})
    assert response.status_code == 401
    data = response.json()
    assert "Session token expired" in data.get("detail", "")
