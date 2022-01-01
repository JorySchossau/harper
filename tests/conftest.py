"""Back-end testing support."""

from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from harper.db import DB, Lesson, Person, Term
from harper.server import app


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
    """Re-initialize the SQLite back-end and return the engine."""
    return DB.configure("sqlite")


@pytest.fixture
def alpha(engine, monday):
    with Session(engine, expire_on_commit=False) as session:
        person = Person(name="Alpha", email="alpha@example.io", created_at=monday)
        session.add(person)
        session.commit()
        return person


@pytest.fixture
def beta(engine, tuesday):
    with Session(engine, expire_on_commit=False) as session:
        person = Person(name="Beta", email="beta@example.io", created_at=tuesday)
        session.add(person)
        session.commit()
        return person


@pytest.fixture
def coding_1(engine, alpha, monday, tuesday):
    with Session(engine, expire_on_commit=False) as session:
        lesson = Lesson(language="en", created_at=tuesday)
        session.add(lesson)
        session.commit() # to set lesson.id
        version = DB.build_lesson_version(session, lesson_id=lesson.id,
                                          title="Coding Lesson", url="https://example.io/coding/",
                                          abstract="Coding lesson abstract", license="CC-BY",
                                          version="1.1", created_at=tuesday)
        version.authors.append(alpha)
        session.add(version)
        term = Term(language="en", term="studying", url="https://wikipedia.org/studying", created_at=monday)
        session.add(term)
        term.lesson_versions.append(version)
        session.commit()
        return lesson


@pytest.fixture
def stats_2(engine, alpha, beta, tuesday, friday):
    with Session(engine, expire_on_commit=False) as session:
        lesson = Lesson(language="en", created_at=tuesday)
        session.add(lesson)
        session.commit() # to set lesson.id
        version_1 = DB.build_lesson_version(session, lesson_id=lesson.id,
                                            title="Stats Lesson", url="https://example.io/stats/",
                                            abstract="Stats lesson abstract", license="CC-BY",
                                            version="1.0", created_at=tuesday)
        version_1.authors.append(alpha)
        session.add(version_1)
        version_2 = DB.build_lesson_version(session, lesson_id=lesson.id,
                                            title="Stats Lesson Revised", url="https://example.io/stats/",
                                            abstract="Stats lesson abstract revised", license="CC-BY",
                                            version="1.1", created_at=friday)
        version_2.authors.append(alpha)
        version_2.authors.append(beta)
        session.add(version_2)
        session.commit()
        return lesson


@pytest.fixture
def client():
    """Create a client for testing the FastAPI server."""
    return TestClient(app)
