"""Test server behavior."""

from datetime import datetime

from sqlalchemy.orm import Session

from harper.db import DB
from harper.util import ErrorMessage

from .util import dict_list_match, error_match


def test_get_status_message(client, engine):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Harper"}


def test_get_no_lessons_when_database_empty(client, engine):
    response = client.get("/lesson/1/")
    assert response.status_code == 404
    assert error_match(response.json()["detail"], ErrorMessage.no_such_lesson)


def test_get_nonexistent_lesson(client, alpha):
    other_id = alpha.id + 1
    response = client.get(f"/lesson/{other_id}/")
    assert error_match(response.json()["detail"], ErrorMessage.no_such_lesson)


def test_get_lesson_when_one_version(client, coding, coding_v1):
    response = client.get(f"/lesson/{coding.id}/")
    assert response.status_code == 200
    body = response.json()
    assert body["lesson_id"] == coding.id
    assert body["sequence_id"] == coding_v1.sequence_id
    assert len(body["authors"]) == 1
    assert len(body["terms"]) == 2
    assert datetime.fromisoformat(body["created_at"]) == coding_v1.created_at


def test_get_lesson_when_two_versions(client, stats, stats_v2):
    response = client.get(f"/lesson/{stats.id}/")
    assert response.status_code == 200
    body = response.json()
    assert body["lesson_id"] == stats.id
    assert body["sequence_id"] == 2
    assert len(body["authors"]) == 2


def test_get_specific_lesson_version(client, stats, stats_v2):
    response = client.get(f"/lesson/{stats.id}/", params={"sequence_id": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["lesson_id"] == stats.id
    assert body["sequence_id"] == 1
    assert len(body["authors"]) == 1


def test_get_all_lessons(client, coding_v1, stats_v2):
    expected_titles = {coding_v1.title, stats_v2.title}
    response = client.get("/lesson/all")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {r["title"] for r in body} == expected_titles


def test_get_existing_person(client, alpha):
    response = client.get(f"/person/{alpha.id}/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == alpha.name
    assert body["email"] == alpha.email


def test_get_nonexistent_person(client, engine):
    response = client.get("/person/1/")
    assert response.status_code == 404
    body = response.json()
    assert error_match(body["detail"], ErrorMessage.no_such_person)


def test_get_all_persons(client, alpha, beta):
    response = client.get("/person/all/")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {p["name"] for p in body} == {alpha.name, beta.name}


def test_get_all_terms(client, coding_v1, stats_v2):
    response = client.get("/term/all/")
    assert response.status_code == 200
    body = response.json()
    expected = [{"term": "studying", "count": 1}, {"term": "musing", "count": 2}]
    assert dict_list_match("term", expected, body)
