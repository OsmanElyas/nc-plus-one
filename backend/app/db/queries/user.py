from app.db.connection import get_connection
from psycopg2.extras import RealDictCursor

def get_user(email):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM users where email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()


    return user

def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM users where user_id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()


    return user

def create_user(name, email, hashed_password):
    conn = get_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("" \
        "INSERT INTO users (name, email, password) " \
        "VALUES (%s,%s,%s)" \
        "RETURNING user_id, name, email, created_at", 
        (name, email, hashed_password)
        )
        
        user = cursor.fetchone()
        conn.commit()

    return user


def check_user_rsvps(user_id):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT events.event_id AS id, events.title, events.starts_at, " \
    "rsvps.created_at AS rsvp_date, " \
    "ROW_NUMBER() OVER (ORDER BY events.starts_at) AS event_rank, " \
    "COUNT(*) OVER () as total_rsvps " \
    " FROM rsvps INNER JOIN events on rsvps.event_id = events.event_id" \
    " where rsvps.attendee_id = %s " \
    "ORDER BY events.starts_at ASC", (user_id,))
    rsvps = cursor.fetchall()

    cursor.close()
    conn.close()


    return rsvps


def get_organiser_stats(organiser_id):
    conn = get_connection()

    try:
    
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """WITH event_attendance AS (
                    SELECT
                        e.event_id,
                        e.organiser_id,
                        COUNT(r.rsvp_id) AS attendee_count
                    FROM events AS e
                    LEFT JOIN rsvps AS r ON r.event_id = e.event_id
                    GROUP BY e.event_id, e.organiser_id
                ),
                organiser_stats AS (
                    SELECT
                        ea.organiser_id,
                        u.name,
                        COUNT(*) AS total_events,
                        ROUND(AVG(ea.attendee_count)::numeric, 1) AS avg_attendance,
                        MAX(ea.attendee_count) AS best_attended_count
                    FROM event_attendance AS ea
                    JOIN users AS u ON u.user_id = ea.organiser_id
                    GROUP BY ea.organiser_id, u.name
                ),
                ranked_organisers AS (
                    SELECT
                        organiser_id,
                        name,
                        total_events,
                        avg_attendance,
                        best_attended_count,
                        RANK() OVER (ORDER BY total_events DESC) AS organiser_rank
                    FROM organiser_stats
                )
                SELECT
                    organiser_id,
                    name,
                    total_events,
                    avg_attendance,
                    best_attended_count,
                    organiser_rank
                FROM ranked_organisers
                WHERE organiser_id = %s""",
                (organiser_id,),
            )
            
            attendees = cursor.fetchone()
            return attendees
    finally:
        conn.close()