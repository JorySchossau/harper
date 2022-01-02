from fastapi import APIRouter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from harper.db import DB, Person
from harper.util import ErrorMessage, HarperExc, harper_exc


router = APIRouter()


@router.get("/{person_id}/")
@harper_exc
async def get_person(person_id):
    """A person."""
    try:
        with Session(DB.engine) as session:
            person = session.query(Person).where(Person.id == person_id).one()
            return {"person_id": person.id, "name": person.name, "email": person.email}
    except NoResultFound:
        raise HarperExc(
            ErrorMessage.no_such_person.format(person_id=person_id), code=404
        )
