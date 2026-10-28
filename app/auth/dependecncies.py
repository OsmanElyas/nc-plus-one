from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.jwt import get_secret
import jwt

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    unauthorised = HTTPException (
        status_code=401,
        detail={"code": "NOT_AUTHENTICATED", "message": "User not authenticated!"},
    )

    if credentials is None:
        raise unauthorised

    try:
        payload = jwt.decode(credentials.credentials, get_secret(), "HS256")
        user_id = int(payload["sub"])
    except:
        raise unauthorised