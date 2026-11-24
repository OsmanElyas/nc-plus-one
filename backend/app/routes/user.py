from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.db.queries.user import check_user_rsvps, get_user_by_id

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me/events", status_code=200)
def get_user_rsvps(user_id: int = Depends(get_current_user)):

    rsvps = check_user_rsvps(user_id)

    return {"events": rsvps}


@user_router.get("/me", status_code=200)
def get_profile(user_id: int = Depends(get_current_user)):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return {
        "user": {
            "id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"],
        }
    }


