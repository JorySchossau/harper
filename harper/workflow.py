"""Operations."""

from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion, Person
from harper.util import ErrorMessage, HarperExc, author_list, term_list


def get_all_lessons():
    """Return the most recent versions of all lessons."""
    with Session(DB.engine) as session:
        subquery = (
            session.query(func.max(LessonVersion.id))
            .group_by(LessonVersion.lesson_id)
            .subquery()
        )
        results = (
            session.query(LessonVersion)
            .filter(LessonVersion.id.in_(subquery.select()))
            .all()
        )
        return [
            {"lesson_id": r.lesson_id, "sequence_id": r.sequence_id, "title": r.title}
            for r in results
        ]


def get_lesson(lesson_id, sequence_id):
    """Get the most recent version of a lesson or a specific version."""
    try:
        with Session(DB.engine) as session:
            if sequence_id is None:
                fmt = ErrorMessage.no_such_lesson
                lv = DB.get_current_lesson_version(session, lesson_id)
            else:
                fmt = ErrorMessage.no_such_lesson_version
                lv = (
                    session.query(LessonVersion)
                    .where(
                        and_(
                            LessonVersion.lesson_id == lesson_id,
                            LessonVersion.sequence_id == sequence_id,
                        )
                    )
                    .one()
                )
            return {
                "lesson_id": lv.lesson_id,
                "sequence_id": lv.sequence_id,
                "created_at": lv.created_at.isoformat(),
                "authors": author_list(lv.authors),
                "terms": term_list(lv.terms),
                "title": lv.title,
                "url": lv.url,
                "version": lv.version,
                "abstract": lv.abstract,
                "license": lv.license,
            }
    except NoResultFound:
        raise HarperExc(
            fmt.format(lesson_id=lesson_id, sequence_id=sequence_id), code=404
        )


def get_person(person_id):
    """Get information about a person."""
    try:
        with Session(DB.engine) as session:
            person = session.query(Person).where(Person.id == person_id).one()
            return {"person_id": person.id, "name": person.name, "email": person.email}
    except NoResultFound:
        raise HarperExc(
            ErrorMessage.no_such_person.format(person_id=person_id), code=404
        )
