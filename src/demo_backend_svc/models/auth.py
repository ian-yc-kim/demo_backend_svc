import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from demo_backend_svc.models.base import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    creation_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # New column for user role with default value 'user'
    role = Column(String, nullable=False, server_default='user')

class Session(Base):
    __tablename__ = 'session'
    session_token = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    expiration_timestamp = Column(DateTime, nullable=False)
