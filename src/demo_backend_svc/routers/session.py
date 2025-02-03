from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from datetime import datetime
import logging
from pydantic import BaseModel

from demo_backend_svc.models.base import get_db
from demo_backend_svc.models.auth import Session as DBSession, User

router = APIRouter()

class SessionResponse(BaseModel):
    username: str
    full_name: str

@router.get("/session", response_model=SessionResponse)

def get_session(
    session_token_header: str = Header(None, alias="session_token"),
    session_token_query: str = Query(None, alias="session_token"),
    db: SQLAlchemySession = Depends(get_db)
):
    token = session_token_header or session_token_query
    if not token:
        raise HTTPException(status_code=401, detail="Session token is missing")
    try:
        session_record = db.query(DBSession).filter(DBSession.session_token == token).first()
        if not session_record:
            raise HTTPException(status_code=401, detail="Invalid session token")
        if session_record.expiration_timestamp <= datetime.utcnow():
            raise HTTPException(status_code=401, detail="Session token expired")
        user_record = db.query(User).filter(User.user_id == session_record.user_id).first()
        if not user_record:
            raise HTTPException(status_code=401, detail="User associated with session not found")
        return SessionResponse(username=user_record.username, full_name=user_record.full_name or "")
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
