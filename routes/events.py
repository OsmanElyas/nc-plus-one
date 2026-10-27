from fastapi import APIRouter, HTTPException
from db.connection import get_connection

events_router = APIRouter(prefix="/events", tags=["events"])

@events_router.get("/", status_code=200)
def list_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute( "SELECT event_id, title, starts_at, ends_at, venues.name FROM events INNER JOIN venues ON venues.venue_id = events.venue_id ORDER BY event_id;")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events":[{"id": event[0], "title": event[1], "starts_at": event[2], "ends_at": event[3], "location": event[4]} for event in events]}

@events_router.get("/{event_id}", status_code=200)
def list_events(event_id: str):
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