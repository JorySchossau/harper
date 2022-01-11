"""Back-end testing support."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from harper.db import DB, Lesson, Person, Term
from harper.server import app


@pytest.fixture
def client():
    """Create a client for testing the FastAPI server."""
    return TestClient(app)


@pytest.fixture
def monday():
    """One of several timestamps."""
    return datetime(2021, 12, 6, 1, 1, 1)


@pytest.fixture
def tuesday():
    """One of several timestamps."""
    return datetime(2021, 12, 7, 2, 2, 2)


@pytest.fixture
def friday():
    """One of several timestamps."""
    return datetime(2021, 12, 10, 3, 3, 3)


@pytest.fixture
def engine():
    """Re-initialize the database."""
    return DB.configure("test")


@pytest.fixture
def session(engine):
    """Re-initialize the database and get a session."""
    return Session(engine)


@pytest.fixture
def alpha(session, monday):
    person = Person(name="Alpha", email="alpha@example.io", created_at=monday)
    session.add(person)
    session.commit()
    return person


@pytest.fixture
def beta(session, tuesday):
    person = Person(name="Beta", email="beta@example.io", created_at=tuesday)
    session.add(person)
    session.commit()
    return person


@pytest.fixture
def studying(session, monday):
    term = Term(
        language="en",
        term="studying",
        url="https://wikipedia.org/studying",
        created_at=monday,
    )
    session.add(term)
    session.commit()
    return term


@pytest.fixture
def musing(session, monday):
    term = Term(
        language="en",
        term="musing",
        url="https://wikipedia.org/musing",
        created_at=monday,
    )
    session.add(term)
    session.commit()
    return term


@pytest.fixture
def coding(session, tuesday):
    lesson = Lesson(language="en", created_at=tuesday)
    session.add(lesson)
    session.commit()
    return lesson


@pytest.fixture
def coding_v1(session, coding, tuesday, alpha, studying, musing):
    version = DB.build_lesson_version(
        session,
        lesson_id=coding.id,
        title="Coding Lesson",
        url="https://example.io/coding/",
        abstract="Coding lesson abstract",
        license="CC-BY",
        version="1.1",
        created_at=tuesday,
    )
    version.authors.append(alpha)
    session.add(version)
    studying.lesson_versions.append(version)
    musing.lesson_versions.append(version)
    session.commit()
    return version


@pytest.fixture
def stats(session, tuesday):
    lesson = Lesson(language="en", created_at=tuesday)
    session.add(lesson)
    session.commit()  # to set lesson.id
    return lesson


@pytest.fixture
def stats_v1(session, stats, tuesday, alpha, musing):
    version = DB.build_lesson_version(
        session,
        lesson_id=stats.id,
        title="Stats Lesson",
        url="https://example.io/stats/",
        abstract="Stats lesson abstract",
        license="CC-BY",
        version="1.0",
        created_at=tuesday,
    )
    version.authors.append(alpha)
    version.terms.append(musing)
    session.add(version)
    return version


@pytest.fixture
def stats_v2(session, stats, stats_v1, alpha, beta, friday, musing):
    version = DB.build_lesson_version(
        session,
        lesson_id=stats.id,
        title="Stats Lesson Revised",
        url="https://example.io/stats/",
        abstract="Stats lesson abstract revised",
        license="CC-BY",
        version="1.1",
        created_at=friday,
    )
    version.authors.append(alpha)
    version.authors.append(beta)
    version.terms.append(musing)
    session.add(version)
    session.commit()
    return version
