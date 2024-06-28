import sys

sys.path.append(".")

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client
