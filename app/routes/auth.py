from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.jwt import create_access_token
from app.db.queries.user import get_user
from app.auth.password import verify_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str



@auth_router.post("/login")
def login(body: LoginRequest):

    if not body.email or not body.password:
        raise HTTPException(
            status_code=400,
            detail="Missing Credentials"             
        )
    
    user = get_user(body.email)


    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
            )
    
    return {
        "access_token": create_access_token(user["user_id"]),
        "token_type": "bearer"
    }

        

    