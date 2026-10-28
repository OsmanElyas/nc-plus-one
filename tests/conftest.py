import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

from app.auth.jwt import create_access_token
from main import app
from app.db.seed import seed


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    seed("test")


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
   
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}






