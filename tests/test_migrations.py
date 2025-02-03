import uuid
from datetime import datetime
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from demo_backend_svc.models.auth import User, Session

def test_tables_created(db_session):
    engine = db_session.bind
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'user' in tables
    assert 'session' in tables


def test_unique_username(db_session):
    try:
        user1 = User(username='testuser', password_hash='hash1', full_name='Test User')
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(username='testuser', password_hash='hash2', full_name='Test User 2')
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    finally:
        db_session.rollback()


def test_foreign_key_constraint(db_session):
    try:
        # Enable foreign key enforcement for SQLite
        db_session.execute(text("PRAGMA foreign_keys=ON"))
        
        # Create a valid user
        user = User(username='user_fk', password_hash='hash', full_name='FK User')
        db_session.add(user)
        db_session.commit()
        
        # Create a valid session
        sess = Session(user_id=user.user_id, expiration_timestamp=datetime.utcnow())
        db_session.add(sess)
        db_session.commit()
        
        db_session.rollback()
        
        # Attempt to create a session with an invalid user_id
        invalid_session = Session(user_id=str(uuid.uuid4()), expiration_timestamp=datetime.utcnow())
        db_session.add(invalid_session)
        with pytest.raises(IntegrityError):
            db_session.commit()
    finally:
        db_session.rollback()


def test_user_default_role(db_session):
    user = User(username='defaultrole', password_hash='hash', full_name='Default Role Test')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.role == 'user'
