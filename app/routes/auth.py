from fastapi import APIRouter, HTTPException
from app.models.auth import LoginRequest, RegisterRequest
from app.auth.jwt import create_access_token
from app.db.queries.user import get_user, create_user
from app.auth.password import hash_password, verify_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])


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

@auth_router.post("/register", status_code=201)
def register_user(user: RegisterRequest):

    existing_user = get_user(user.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = create_user(user.name, user.email, hashed_password)

    return {"user": new_user}