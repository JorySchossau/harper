"""Back-end testing support."""

import pytest

from harper.db import DB


@pytest.fixture
def engine():
    """Re-initialize the SQLite back-end and return the engine."""
    return DB.configure("sqlite")
