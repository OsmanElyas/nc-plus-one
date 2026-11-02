from fastapi import APIRouter, HTTPException, Depends
from app.db.connection import get_connection
from psycopg2.extras import RealDictCursor
from app.auth.dependencies import get_current_user



def create_rsvp(user_id, event_id):
    conn = get_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "INSERT INTO rsvps (attendee_id, event_id) VALUES (%s, %s) "
            "RETURNING rsvp_id, attendee_id, event_id, created_at",
            (user_id, event_id),
        )
        rsvp = cursor.fetchone()
        conn.commit()

    conn.close()

    return rsvp


def check_rsvp(attendee_id, event_id):
    conn = get_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT FROM rsvps "
            "WHERE attendee_id = %s and event_id = %s",
            (attendee_id, event_id),
        )
        rsvp = cursor.fetchone()
        conn.commit()

    conn.close()

    return rsvp

def delete_rsvp(user_id, event_id):
    conn = get_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "DELETE FROM rsvps "
            "WHERE attendee_id = %s and event_id = %s",
            (user_id, event_id),
        )
        
        conn.commit()

    conn.close()


def check_event_attendees(event_id):
    conn = get_connection()

    try:

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT rsvps.attendee_id as id, users.name, users.email FROM rsvps INNER JOIN users ON rsvps.attendee_id = users.user_id "
                "WHERE rsvps.event_id = %s",
                (event_id,),
            )
            
            attendees = cursor.fetchall()
            return attendees
    finally:
        conn.close()


