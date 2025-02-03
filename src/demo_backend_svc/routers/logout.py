import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from demo_backend_svc.models.auth import Session as SessionModel
from demo_backend_svc.models.base import get_db

router = APIRouter()

@router.post("/")
def logout(authorization: str = Header(None, alias="Authorization"), db: Session = Depends(get_db)):
    if not authorization:
        logging.error("Missing session token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing session token")
    
    # Extract token from the Authorization header; expect format: 'Bearer <token>'
    token = authorization.replace("Bearer", "").strip()
    
    session_record = db.query(SessionModel).filter(SessionModel.session_token == token).first()
    if not session_record:
        logging.error("Invalid session token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
    
    if session_record.expiration_timestamp < datetime.utcnow():
        logging.error("Session token expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token expired")
    
    try:
        db.delete(session_record)
        db.commit()
        return {"message": "Logout successful"}
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
