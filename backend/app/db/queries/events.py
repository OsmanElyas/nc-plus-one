from app.db.connection import get_connection
from psycopg2.extras import RealDictCursor

def get_event_by_id(event_id):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM events where event_id = %s", (event_id,))
            event = cursor.fetchone()
        return event
    finally:
        conn.close()

    
def create_event(title, description, starts_at, ends_at, organiser_id, venue_id):

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO events
                    (title, description, starts_at, ends_at, organiser_id, venue_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING event_id, title, description, starts_at, ends_at,
                            organiser_id, venue_id, created_at
                """,
                (title, description, starts_at, ends_at, organiser_id, venue_id),
            )
            event = cursor.fetchone()
        conn.commit()
        return event
    finally:
        conn.close()


def update_event_query(event_id, updates):

    conn = get_connection()

    allowed_fields = {"description", "starts_at", "ends_at"}

    set_parts = []
    values = []

    for field, value in updates.items():
        if field in allowed_fields:
            set_parts.append(f"{field} = %s")
            values.append(value)
    values.append(event_id)

    if not set_parts:
        return None

    query = f"UPDATE events SET {', '.join(set_parts)} WHERE event_id = %s RETURNING *"


    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, values)
            updated_event = cursor.fetchone()
        conn.commit()

        return updated_event
    finally:
        conn.close()