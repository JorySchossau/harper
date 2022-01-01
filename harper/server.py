"""Main server script."""

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion, Person
from harper.util import ErrorMessage, author_list, term_list

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Harper"}


@app.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id, sequence_id=None):
    with Session(DB.engine) as session:
        try:
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
            msg = fmt.format(lesson_id=lesson_id, sequence_id=sequence_id)
            raise HTTPException(status_code=404, detail=msg)


@app.get("/person/{person_id}")
async def get_person(person_id):
    with Session(DB.engine) as session:
        try:
            person = session.query(Person).where(Person.id == person_id).one()
        except NoResultFound:
            msg = ErrorMessage.no_such_person.format(person_id=person_id)
            raise HTTPException(status_code=404, detail=msg)
        return {"person_id": person.id, "name": person.name, "email": person.email}


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.server:app", host="0.0.0.0", port=80, reload=True)
