import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Depends

from demo_backend_svc.models.base import get_db
from demo_backend_svc.models.auth import Session

router = APIRouter()

@router.post("/logout")

def logout(request: Request, db=Depends(get_db)):
    """Endpoint to logout a user by invalidating the session token."""
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing session token")
    # Remove Bearer prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        session_entry = db.query(Session).filter(Session.session_token == token).first()
        if not session_entry:
            raise HTTPException(status_code=401, detail="Invalid session token")
        # Check if session is already expired
        if session_entry.expiration_timestamp < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Session token expired")
        # Invalidate the session by deleting the record
        db.delete(session_entry)
        db.commit()
        return {"message": "Logout successful"}
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
