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


def test_get_lesson_when_database_has_one(engine, client, lesson_coding_1):
    with Session(engine) as session:
        retrieved = session.query(Lesson).where(Lesson.id == lesson_coding_1.id).one()
        created_at = retrieved.versions[0].created_at
    response = client.get("/lesson/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["authors"] == []
    assert len(body["terms"]) == 1
    assert datetime.fromisoformat(body["created_at"]) == created_at
