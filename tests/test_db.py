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


def test_create_person(engine):
    with Session(engine) as session:
        person = Person(name="Alpha Beta", email="alpha@beta.io")
        session.add(person)
        session.commit()

    with Session(engine) as session:
        persons = session.query(Person).all()
        assert len(persons) == 1
        assert persons[0].id == 1
        assert persons[0].name == "Alpha Beta"
        assert persons[0].email == "alpha@beta.io"


def test_create_lesson(engine):
    with Session(engine) as session:
        session.add(Lesson(language="en"))
        session.add(DB.build_lesson_version(session, lesson_id=1))
        session.add(DB.build_lesson_version(session, lesson_id=1))
        session.commit()

    with Session(engine) as session:
        lessons = session.query(Lesson).all()
        assert lessons[0].id == 1

        versions = session.query(LessonVersion).all()
        assert len(versions) == 2
        assert {1, 2} == {v.sequence_id for v in versions}


def test_different_lessons_have_different_sequence_ids(engine):
    with Session(engine) as session:
        lesson_1 = Lesson(language="en")
        session.add(lesson_1)
        session.add(DB.build_lesson_version(session, lesson_id=1))
        lesson_2 = Lesson(language="en")
        session.add(lesson_2)
        session.add(DB.build_lesson_version(session, lesson_id=2))
        session.commit()

    with Session(engine) as session:
        versions = session.query(LessonVersion).all()
        assert len(versions) == 2
        assert {(1, 1), (2, 1)} == {(v.lesson_id, v.sequence_id) for v in versions}


def test_deleting_lesson_deletes_versions(engine):
    with Session(engine) as session:
        session.add(Lesson(language="en"))
        session.add(DB.build_lesson_version(session, lesson_id=1))
        session.commit()

        assert len(session.query(Lesson).all()) == 1
        assert len(session.query(LessonVersion).all()) == 1

        lesson = session.query(Lesson).filter_by(id=1).first()
        session.delete(lesson)
        session.commit()

        assert len(session.query(Lesson).all()) == 0
        assert len(session.query(LessonVersion).all()) == 0


def test_get_most_recent_version_of_lesson(engine):
    lesson_id = None
    with Session(engine) as session:
        lesson = Lesson(language="en")
        session.add(lesson)
        for i in range(3):
            session.add(DB.build_lesson_version(session, lesson_id=1))
        session.commit()
        lesson_id = lesson.id

    with Session(engine) as session:
        subquery = (
            session.query(func.max(LessonVersion.id))
            .filter(LessonVersion.lesson_id == lesson_id)
            .scalar_subquery()
        )
        query = session.query(LessonVersion).filter(
            LessonVersion.lesson_id == lesson_id, LessonVersion.id == subquery
        )
        records = query.all()
        assert len(records) == 1
        assert records[0].lesson_id == 1
        assert records[0].id == 3


def test_lesson_version_authors(engine):
    with Session(engine) as session:
        person_1 = Person(name="Alpha", email="alpha@example.io")
        session.add(person_1)
        lesson = Lesson(language="en")
        session.add(lesson)
        version_1 = DB.build_lesson_version(session, lesson_id=1)
        session.add(version_1)
        version_1.authors.append(person_1)

        person_2 = Person(name="Beta", email="beta@example.io")
        session.add(person_2)
        version_2 = DB.build_lesson_version(session, lesson_id=1)
        session.add(version_2)
        version_2.authors.append(person_1)
        version_2.authors.append(person_2)

        session.commit()

    with Session(engine) as session:
        person = session.query(Person).where(Person.id == 1).one()
        assert len(person.lesson_versions) == 2
        assert {v.id for v in person.lesson_versions} == {1, 2}

        v1 = session.query(LessonVersion).where(LessonVersion.id == 1).one()
        assert len(v1.authors) == 1
        v2 = session.query(LessonVersion).where(LessonVersion.id == 2).one()
        assert len(v2.authors) == 2


def test_lesson_version_terms(engine):
    with Session(engine) as session:
        session.add(Lesson(language="en"))
        version = DB.build_lesson_version(session, lesson_id=1)
        session.add(version)
        term = Term(language="es", term="ensayo", url="https://wikipedia.org/something")
        session.add(term)
        term.lesson_versions.append(version)
        session.commit()

    with Session(engine) as session:
        lesson = session.query(Lesson).one()
        assert len(lesson.versions[0].terms) == 1
        term = lesson.versions[0].terms[0]
        assert term.term == "ensayo"
