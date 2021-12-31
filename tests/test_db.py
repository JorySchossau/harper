from sqlalchemy.orm import Session

from harper.db import Lesson, LessonVersion, Person


def test_all_tables_initially_empty(engine):
    with Session(engine) as session:
        assert len(session.query(Lesson).all()) == 0
        assert len(session.query(LessonVersion).all()) == 0
        assert len(session.query(Person).all()) == 0
