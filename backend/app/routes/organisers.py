from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.db.queries.user import get_organiser_stats

organisers_router = APIRouter(prefix="/organisers", tags=["organisers"])


@organisers_router.get("/{organiser_id}/stats", status_code=200, dependencies=[Depends(get_current_user)])
def get_organiser(organiser_id: int):

    stats = get_organiser_stats(organiser_id)

    if stats is None:
        raise HTTPException(status_code=404, detail="Organiser not found")


    return {"stats": stats}


