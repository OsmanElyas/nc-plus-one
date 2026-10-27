import psycopg2
import os
from dotenv import load_dotenv



def get_connection():
    load_dotenv(".env")
    
    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE not set")

    
    connection = psycopg2.connect()
    return connection

def get_test_connection():
    load_dotenv(".env.test", override=True)
    
    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE not set")

    connection = psycopg2.connect()
    return connection



if __name__ == "__main__":
    connection = get_connection()
    print("connected successfully")
    connection.close()