from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.db.queries.user import check_user_rsvps

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me/events", status_code=200)
def get_user_rsvps(user_id: int = Depends(get_current_user)):

    rsvps = check_user_rsvps(user_id)

    return {"events": rsvps}


