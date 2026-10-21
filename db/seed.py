import json
from connection import get_connection


def drop_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS rsvps;")
    cursor.execute("DROP TABLE IF EXISTS events;")
    cursor.execute("DROP TABLE IF EXISTS venues;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    

def load_data(filepath):
    with open(f"db/data/{filepath}.json") as file:
        data = json.load(file)

    return data

def create_tables(cursor):
    cursor.execute(
        "CREATE TABLE users (" \
        "user_id SERIAL PRIMARY KEY," \
        "email VARCHAR UNIQUE NOT NULL," \
        "password VARCHAR NOT NULL," \
        "name VARCHAR NOT NULL," \
        "created_at TIMESTAMP DEFAULT NOW()" \
        ");"
    )

    cursor.execute(
        "CREATE TABLE venues (" \
        "venue_id SERIAL PRIMARY KEY," \
        "name VARCHAR(255) NOT NULL," \
        "address TEXT," \
        "capacity INT" \
        ");"
        )

    cursor.execute(
        "CREATE TABLE events (" \
        "event_id SERIAL PRIMARY KEY,"
        "title VARCHAR(255) NOT NULL," \
        "description VARCHAR," \
        "starts_at DATE NOT NULL," \
        "ends_at DATE NOT NULL," \
        "organiser_id INT REFERENCES users(user_id)," \
        "venue_id INT REFERENCES venues(venue_id)," \
        "created_at TIMESTAMP DEFAULT NOW()" \
        ");"
        )

    cursor.execute(
        "CREATE TABLE rsvps (" \
        "rsvp_id SERIAL PRIMARY KEY," \
        "attendee_id INT REFERENCES users(user_id)," \
        "event_id INT REFERENCES events(event_id)," \
        "created_at TIMESTAMP DEFAULT NOW()" \
        ");"
    )
    


    

def insert_users(cursor):
    users = load_data("users")

    for user in users:
        cursor.execute(
            "INSERT INTO users (email, password, name) VALUES (%s, %s, %s);", 
            (user["email"], user["password"], user["name"])
        )

def insert_venues(cursor):
    venues = load_data("venues")

    for venue in venues:
        cursor.execute(
            "INSERT INTO venues (name, address, capacity) VALUES (%s, %s, %s);", 
            (venue["name"], venue["address"], venue["capacity"])
        )

def insert_events(cursor):
    events = load_data("events")

    for event in events:
        cursor.execute(
            "INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s);", 
            (event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"])
        )


def insert_rsvps(cursor):
    rsvps = load_data("rsvps")

    for rsvp in rsvps:
        cursor.execute(
            "INSERT INTO rsvps (attendee_id, event_id) VALUES (%s, %s);", 
            (rsvp["attendee_id"], rsvp["event_id"])
        )

    

def seed():
    connection = get_connection()
    cursor = connection.cursor()

    drop_tables(cursor)
    create_tables(cursor)

    insert_users(cursor)
    insert_venues(cursor)
    insert_events(cursor)
    insert_rsvps(cursor)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    seed()