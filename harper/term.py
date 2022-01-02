"""Handle requests for information about terms."""

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion, Term
from harper.util import harper_exc

router = APIRouter()


@router.get("/all/")
@harper_exc
async def get_all_terms():
    """All terms with frequency count."""
    with Session(DB.engine) as session:
        subquery = session.query(func.max(LessonVersion.id))
        subquery = subquery.group_by(LessonVersion.lesson_id)
        subquery = subquery.subquery()

        query = session.query(Term, func.count(Term.id))
        query = query.select_from(LessonVersion)
        query = query.join(LessonVersion.terms)
        query = query.group_by(Term.id)
        query = query.filter(LessonVersion.id.in_(subquery.select()))

        results = query.all()
        return [r[0].to_dict() | {"count": r[1]} for r in results]
