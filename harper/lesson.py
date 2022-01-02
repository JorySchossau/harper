from fastapi import APIRouter, HTTPException
from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion
from harper.util import ErrorMessage, HarperExc, harper_exc, author_list, term_list


router = APIRouter()


@router.get("/all/")
@harper_exc
async def get_all_lessons():
    """Get the most recent versions of all lessons."""
    with Session(DB.engine) as session:
        subquery = session.query(func.max(LessonVersion.id))
        subquery = subquery.group_by(LessonVersion.lesson_id)
        subquery = subquery.subquery()

        query = session.query(LessonVersion)
        query = query.filter(LessonVersion.id.in_(subquery.select()))

        results = query.all()
        return [r.to_dict() for r in results]


@router.get("/{lesson_id}/")
@harper_exc
async def get_lesson(lesson_id, sequence_id=None):
    """A specific (version of a) lesson."""
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
            return lv.to_dict() | {"authors": author_list(lv.authors), "terms": term_list(lv.terms)}
    except NoResultFound:
        raise HarperExc(
            fmt.format(lesson_id=lesson_id, sequence_id=sequence_id), code=404
        )
