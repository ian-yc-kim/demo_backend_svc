import uuid
import bcrypt
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from demo_backend_svc.models.base import get_db
from demo_backend_svc.models.auth import User, Session


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_token: str


@router.post("", response_model=LoginResponse)

def login(request: LoginRequest, db=Depends(get_db)):
    try:
        # Retrieve the user by username
        user = db.query(User).filter(User.username == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        # Verify the password using bcrypt
        if not bcrypt.checkpw(request.password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        # Generate a new session token
        session_token = str(uuid.uuid4())
        expiration_timestamp = datetime.utcnow() + timedelta(days=7)

        # Create a new session record
        new_session = Session(
            session_token=session_token,
            user_id=user.user_id,
            expiration_timestamp=expiration_timestamp
        )
        db.add(new_session)
        db.commit()

        return LoginResponse(session_token=session_token)
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
