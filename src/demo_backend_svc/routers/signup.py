import re
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
import bcrypt

from demo_backend_svc.models.auth import User
from demo_backend_svc.models.base import get_db

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    password: str
    full_name: str | None = None

    @validator("username")
    def validate_username(cls, v: str) -> str:
        # Username must be 3-30 characters long; only alphanumeric and underscores allowed
        if not re.match(r'^[A-Za-z0-9_]{3,30}$', v):
            raise ValueError("Username must be 3-30 characters long and can contain alphanumeric characters and underscores only")
        return v

    @validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[\W_]', v):
            raise ValueError("Password must contain at least one special character")
        return v

class SignupResponse(BaseModel):
    user_id: str
    username: str
    role: str

# Updated route: removed duplicate '/signup' so that with prefix it resolves to '/signup'
@router.post("", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)

def signup(signup_data: SignupRequest, db: Session = Depends(get_db)) -> SignupResponse:
    try:
        # Check if the username already exists
        existing_user = db.query(User).filter(User.username == signup_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(signup_data.password.encode('utf-8'), salt)
        
        new_user = User(
            username=signup_data.username,
            password_hash=hashed_password.decode('utf-8'),
            full_name=signup_data.full_name,
            creation_timestamp=datetime.utcnow(),
            role='user'  # explicitly set role attribute to 'user'
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logging.info(f"User created successfully: username={new_user.username}, user_id={new_user.user_id}")
        return SignupResponse(user_id=new_user.user_id, username=new_user.username, role=new_user.role)
    except HTTPException as http_exc:
        logging.error(http_exc, exc_info=True)
        raise http_exc
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
