"""Test server behavior."""

from datetime import datetime

from sqlalchemy.orm import Session

from harper.db import DB, Lesson, LessonVersion
from harper.util import ErrorMessage

from .util import error_match


def test_get_status_message(engine, client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Harper"}


def test_get_no_lessons_when_database_empty(engine, client):
    response = client.get("/lesson/1")
    assert response.status_code == 404
    assert error_match(response.json()["detail"], ErrorMessage.no_such_lesson)


def test_get_nonexistent_lesson(engine, client, alpha):
    other_id = alpha.id + 1
    response = client.get(f"/lesson/{other_id}")
    assert error_match(response.json()["detail"], ErrorMessage.no_such_lesson)


def test_get_lesson_when_one_version(engine, client, coding_1):
    with Session(engine) as session:
        retrieved = DB.get_current_lesson_version(session, coding_1.id)
        created_at = retrieved.created_at

        response = client.get(f"/lesson/{coding_1.id}")
        assert response.status_code == 200
        body = response.json()
        assert body["lesson_id"] == retrieved.lesson_id
        assert body["sequence_id"] == retrieved.sequence_id
        assert len(body["authors"]) == 1
        assert len(body["terms"]) == 1
        assert datetime.fromisoformat(body["created_at"]) == created_at


def test_get_lesson_when_two_versions(engine, client, stats_2):
    with Session(engine) as session:
        retrieved = DB.get_current_lesson_version(session, stats_2.id)

        response = client.get(f"/lesson/{stats_2.id}")
        assert response.status_code == 200
        body = response.json()
        assert body["lesson_id"] == retrieved.lesson_id
        assert body["sequence_id"] == 2
        assert len(body["authors"]) == 2


def test_get_specific_lesson_version(engine, client, stats_2):
    with Session(engine) as session:
        response = client.get(f"/lesson/{stats_2.id}", params={"sequence_id": 1})
        assert response.status_code == 200
        body = response.json()
        assert body["lesson_id"] == stats_2.id
        assert body["sequence_id"] == 1
        assert len(body["authors"]) == 1


def test_get_existing_person(engine, client, alpha):
    with Session(engine) as session:
        response = client.get(f"/person/{alpha.id}")
        assert response.status_code == 200
        body = response.json()
        assert body["name"] == alpha.name
        assert body["email"] == alpha.email


def test_get_nonexistent_person(engine, client):
    with Session(engine) as session:
        response = client.get(f"/person/1")
        assert response.status_code == 404
        body = response.json()
        assert error_match(response.json()["detail"], ErrorMessage.no_such_person)
