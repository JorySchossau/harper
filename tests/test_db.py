"""Test database operations."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from harper.db import DB, Lesson, LessonVersion, Person, Term


def test_all_tables_initially_empty(engine):
    with Session(engine) as session:
        assert len(session.query(Lesson).all()) == 0
        assert len(session.query(LessonVersion).all()) == 0
        assert len(session.query(Person).all()) == 0


def test_create_person(engine, person_alpha):
    with Session(engine) as session:
        persons = session.query(Person).all()
        assert len(persons) == 1
        assert persons[0].id == person_alpha.id
        assert persons[0].name == person_alpha.name
        assert persons[0].email == person_alpha.email


def test_create_lesson(engine, lesson_stats_2):
    with Session(engine) as session:
        lessons = session.query(Lesson).all()
        assert lessons[0].id == lesson_stats_2.id
        versions = session.query(LessonVersion).all()
        assert len(versions) == 2
        assert {1, 2} == {v.sequence_id for v in versions}


def test_different_lessons_have_different_sequence_ids(engine, lesson_coding_1, lesson_stats_2):
    with Session(engine) as session:
        versions = session.query(LessonVersion).all()
        assert len(versions) == 3
        assert {(1, 1), (2, 1), (2, 2)} == {(v.lesson_id, v.sequence_id) for v in versions}


def test_deleting_lesson_deletes_versions(engine, lesson_coding_1, lesson_stats_2):
    with Session(engine) as session:
        session.delete(lesson_stats_2)
        session.commit()
        assert len(session.query(Lesson).all()) == 1
        assert len(session.query(LessonVersion).all()) == 1


def test_get_most_recent_version_of_lesson(engine, lesson_stats_2):
    with Session(engine) as session:
        lv = DB.get_current_lesson_version(session, lesson_stats_2.id)
        assert lv.sequence_id == 2


def test_lesson_version_authors(engine, person_alpha, person_beta, lesson_stats_2):
    with Session(engine) as session:
        lesson = session.query(Lesson).where(Lesson.id == lesson_stats_2.id).one()
        lesson.versions[0].authors.append(person_alpha)
        lesson.versions[1].authors.append(person_alpha)
        lesson.versions[1].authors.append(person_beta)
        session.commit()

        person = session.query(Person).where(Person.id == person_alpha.id).one()
        assert len(person.lesson_versions) == 2
        assert {v.sequence_id for v in person.lesson_versions} == {1, 2}

        versions = session.query(LessonVersion).where(LessonVersion.lesson_id == lesson_stats_2.id).order_by(LessonVersion.sequence_id)
        assert len(versions[0].authors) == 1
        assert len(versions[1].authors) == 2


def test_lesson_version_terms(engine, lesson_coding_1):
    with Session(engine) as session:
        lesson = session.query(Lesson).one()
        assert len(lesson.versions[0].terms) == 1
        term = lesson.versions[0].terms[0]
        assert term.term == "studying"
