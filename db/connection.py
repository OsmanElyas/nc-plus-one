import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(".env")

def get_connection():
    
    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE not set")

    
    connection = psycopg2.connect()
    return connection


if __name__ == "__main__":
    connection = get_connection()
    print("connected successfully")
    connection.close()