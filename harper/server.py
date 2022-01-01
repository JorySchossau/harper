"""Main server script."""

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from harper.db import DB, LessonVersion
from harper.util import ErrorMessage, author_list, term_list

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Harper"}


@app.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id, sequence_id=None):
    with Session(DB.engine) as session:
        if sequence_id is None:
            lv = DB.get_current_lesson_version(session, lesson_id)
            if lv is None:
                msg = ErrorMessage.no_such_lesson.format(lesson_id=lesson_id)
                raise HTTPException(status_code=404, detail=msg)
        else:
            lv = session.query(LessonVersion).where(and_(LessonVersion.lesson_id == lesson_id,
                                                         LessonVersion.sequence_id == sequence_id)).one()
            if lv is None:
                msg = ErrorMessage.no_such_lesson_version.format(lesson_id=lesson_id, sequence_id=sequence_id)
                raise HTTPException(status_code=404, detail=msg)
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
            "license": lv.license
        }


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.main:app", host="0.0.0.0", port=80, reload=True)
