from fastapi import APIRouter, HTTPException, Depends
from app.db.connection import get_connection
from app.db.queries.rsvp import create_rsvp, check_rsvp, delete_rsvp, check_event_attendees
from app.auth.dependencies import get_current_user
from app.db.queries.events import get_event_by_id
from app.models.events import EventRequest
from app.db.queries.events import create_event as insert_function, update_event_query

events_router = APIRouter(prefix="/events", tags=["events"])

@events_router.get("", status_code=200, dependencies=[Depends(get_current_user)])
def list_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute( "SELECT event_id, title, starts_at, ends_at, venues.name FROM events INNER JOIN venues ON venues.venue_id = events.venue_id ORDER BY event_id;")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events":[{"id": event[0], "title": event[1], "starts_at": event[2], "ends_at": event[3], "location": event[4]} for event in events]}

@events_router.get("/{event_id}", status_code=200, dependencies=[Depends(get_current_user)])
def get_event(event_id: str):
    if not event_id.isdigit():
        raise HTTPException(status_code=400, detail={"code": "BAD REQUEST", "message": "ID MUST BE A Valid Integer!"})
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute( "SELECT event_id, description, title, starts_at, ends_at, venues.name, address, capacity, created_at " \
    "FROM events INNER JOIN venues ON venues.venue_id = events.venue_id " \
    "WHERE event_id = %s;",
    (event_id,)
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="ROW IS NOT FOUND")

    cursor.close()
    conn.close()
    return {"id": row[0],"description": row[1], "title": row[2], "starts_at": row[3], "ends_at": row[4], "location": row[5], "address": row[6], "capacity": row[7], "created_at": row[8]}



@events_router.post("/{event_id}/rsvp", status_code=201)
def create_event_rsvp(event_id: str, user_id = Depends(get_current_user)):
    event = get_event_by_id(event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event is not found")

    already_rsvp = check_rsvp(user_id, event_id)

    if already_rsvp:
        raise HTTPException(status_code=409, detail="User is already RSVP'd")

    

    rsvp = create_rsvp(user_id, event_id)

    return {"rsvp": rsvp}


@events_router.delete("/{event_id}/rsvp/me", status_code=204)
def delete_event_my_rsvp(event_id: str, user_id = Depends(get_current_user)):


    already_rsvp = check_rsvp(user_id, event_id)

    if not already_rsvp:
        raise HTTPException(status_code=404, detail="RSVP does not exist")

    

    rsvp = delete_rsvp(user_id, event_id)

    return {"rsvp": rsvp}

@events_router.post("", status_code=201)
def create_event(event: EventRequest, organiser_id = Depends(get_current_user)):


    created_event = insert_function(
        title=event.title,
        description=event.description, 
        starts_at=event.starts_at, 
        ends_at=event.ends_at, 
        organiser_id=organiser_id, 
        venue_id=event.venue_id
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event is not found")

    return {"event": created_event}


@events_router.patch("/{event_id}", status_code=201)
def update_event(event_id:int, updates: dict, user_id = Depends(get_current_user)):
    event = get_event_by_id(user_id)

    if not event:
            raise HTTPException(status_code=404, detail="Event is not found")

    if event["organiser_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")


    updated_event = update_event_query(event_id, updates, user_id)

    return {"event": updated_event}

@events_router.get("/{event_id}/attendees", status_code=200)
def check_attendees(event_id:int, user_id = Depends(get_current_user)):

    event = get_event_by_id(event_id)
    

    if not event:
        raise HTTPException(status_code=404, detail="Event is not found")
         
    if event["organiser_id"] != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

    attendees = check_event_attendees(event_id)


    return {"attendees": attendees}