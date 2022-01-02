"""Test database operations."""

from harper.db import DB, Lesson, LessonVersion, Person


def test_create_person(session, alpha):
    persons = session.query(Person).all()
    assert len(persons) == 1
    assert persons[0].id == alpha.id
    assert persons[0].name == alpha.name
    assert persons[0].email == alpha.email


def test_all_tables_initially_empty(session):
    assert len(session.query(Lesson).all()) == 0
    assert len(session.query(LessonVersion).all()) == 0
    assert len(session.query(Person).all()) == 0


def test_create_lesson(session, stats, stats_v2):
    lessons = session.query(Lesson).all()
    assert lessons[0].id == stats.id
    versions = session.query(LessonVersion).all()
    assert len(versions) == 2
    assert {1, 2} == {v.sequence_id for v in versions}


def test_different_lessons_separate_sequence_ids(session, coding_v1, stats_v2):
    versions = session.query(LessonVersion).all()
    assert len(versions) == 3
    assert {(1, 1), (2, 1), (2, 2)} == {(v.lesson_id, v.sequence_id) for v in versions}


def test_deleting_lesson_deletes_versions(session, stats, coding_v1, stats_v2):
    session.delete(stats)
    session.commit()
    assert len(session.query(Lesson).all()) == 1
    assert len(session.query(LessonVersion).all()) == 1


def test_get_most_recent_version_of_lesson(session, stats, stats_v2):
    lv = DB.get_current_lesson_version(session, stats.id)
    assert lv.sequence_id == stats_v2.sequence_id


def test_lesson_version_authors(session, alpha, beta, stats, stats_v2):
    person = session.query(Person).where(Person.id == alpha.id).one()
    assert len(person.lesson_versions) == 2
    assert {v.sequence_id for v in person.lesson_versions} == {1, 2}

    versions = (
        session.query(LessonVersion)
        .where(LessonVersion.lesson_id == stats.id)
        .order_by(LessonVersion.sequence_id)
    )
    assert len(versions[0].authors) == 1
    assert len(versions[1].authors) == 2


def test_lesson_version_terms(session, coding_v1, studying, musing):
    lesson = session.query(Lesson).one()
    assert len(lesson.versions) == 1
    assert len(lesson.versions[0].terms) == 2
    actual = {t.term for t in lesson.versions[0].terms}
    assert actual == {studying.term, musing.term}
