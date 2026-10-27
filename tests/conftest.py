
import pytest
from fastapi.testclient import TestClient

from main import app

#conn = get_test_connection()

@pytest.fixture
def client():
    return TestClient(app)






