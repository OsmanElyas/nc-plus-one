import psycopg2
import os
from dotenv import load_dotenv



def get_connection(environment="dev"):
    
    load_dotenv(f".env.{environment}")
    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE not set")

    
    connection = psycopg2.connect()
    return connection




