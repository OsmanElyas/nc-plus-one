import json
from app.db.connection import get_connection
from app.auth.password import hash_password
import sys

def drop_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS rsvps;")
    cursor.execute("DROP TABLE IF EXISTS events;")
    cursor.execute("DROP TABLE IF EXISTS venues;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    

def load_data(filename, environment):
    with open(f"data/{environment}/{filename}.json") as file:
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
    

def insert_users(cursor, environment):
    users = load_data("users", environment)

    for user in users:
        cursor.execute(
            "INSERT INTO users (email, password, name) VALUES (%s, %s, %s);", 
            (user["email"], hash_password(user["password"]), user["name"])
        )

def insert_venues(cursor, environment):
    venues = load_data("venues", environment)

    for venue in venues:
        cursor.execute(
            "INSERT INTO venues (name, address, capacity) VALUES (%s, %s, %s);", 
            (venue["name"], venue["address"], venue["capacity"])
        )

def insert_events(cursor, environment):
    events = load_data("events", environment)

    for event in events:
        cursor.execute(
            "INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s);", 
            (event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"])
        )


def insert_rsvps(cursor, environment):
    rsvps = load_data("rsvps", environment)

    for rsvp in rsvps:
        cursor.execute(
            "INSERT INTO rsvps (attendee_id, event_id) VALUES (%s, %s);", 
            (rsvp["attendee_id"], rsvp["event_id"])
        )

    

def seed(environment="dev"):
    connection = get_connection(environment)
    cursor = connection.cursor()

    drop_tables(cursor)
    create_tables(cursor)

    insert_users(cursor, environment)
    insert_venues(cursor, environment)
    insert_events(cursor, environment)
    insert_rsvps(cursor, environment)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    environment = sys.argv[1] if len(sys.argv) > 1 else "dev"
    seed(environment)