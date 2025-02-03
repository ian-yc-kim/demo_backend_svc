import json
from datetime import datetime, timedelta
import uuid

import pytest
from fastapi import status

from demo_backend_svc.models.auth import User, Session


def create_user(db, username="testuser", full_name="Test User"):
    user = User(
        user_id=str(uuid.uuid4()),
        username=username,
        password_hash="dummyhash",
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_session(db, user_id, valid=True):
    expiration = datetime.utcnow() + timedelta(hours=1) if valid else datetime.utcnow() - timedelta(hours=1)
    session = Session(
        session_token=str(uuid.uuid4()),
        user_id=user_id,
        expiration_timestamp=expiration
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def test_missing_token(client):
    response = client.get("/auth/session")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "Session token is missing" in data.get("detail")


def test_invalid_token(client, db_session):
    # No session created with this token
    invalid_token = str(uuid.uuid4())
    response = client.get("/auth/session", headers={"session_token": invalid_token})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "Invalid session token" in data.get("detail")


def test_expired_token(client, db_session):
    db = db_session
    user = create_user(db)
    expired_session = create_session(db, user.user_id, valid=False)
    response = client.get("/auth/session", headers={"session_token": expired_session.session_token})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "Session token expired" in data.get("detail")


def test_valid_token(client, db_session):
    db = db_session
    user = create_user(db, username="validuser", full_name="Valid User")
    valid_session = create_session(db, user.user_id, valid=True)
    response = client.get("/auth/session", headers={"session_token": valid_session.session_token})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get("username") == "validuser"
    assert data.get("full_name") == "Valid User"
