import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

from app.auth.jwt import create_access_token
from main import app
from app.db.seed import seed
from app.db.seed import seed
from app.db.connection import get_connection


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    seed("test")


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_cleanup():
    statements = []

    def register_cleanup(sql, params=()):
        statements.append((sql, params))

    yield register_cleanup

    if not statements:
        return

    conn = get_connection("test")
    try:
        with conn.cursor() as cursor:
            for sql, params in reversed(statements):
                cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()

@pytest.fixture
def auth_headers():
   
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}






