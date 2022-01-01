from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion, Person
from harper.util import ErrorMessage, HarperExc, author_list, term_list

def get_lesson(lesson_id, sequence_id):
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
        raise HarperExc(fmt.format(lesson_id=lesson_id, sequence_id=sequence_id))


def get_person(person_id):
    try:
        with Session(DB.engine) as session:
            person = session.query(Person).where(Person.id == person_id).one()
            return {"person_id": person.id, "name": person.name, "email": person.email}
    except NoResultFound:
        raise HarperExc(ErrorMessage.no_such_person.format(person_id=person_id))
