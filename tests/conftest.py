"""Back-end testing support."""

import pytest
from fastapi.testclient import TestClient

from harper.db import DB
from harper.server import app


@pytest.fixture
def engine():
    """Re-initialize the SQLite back-end and return the engine."""
    return DB.configure("sqlite")


@pytest.fixture
def client():
    """Create a client for testing the FastAPI server."""
    return TestClient(app)
