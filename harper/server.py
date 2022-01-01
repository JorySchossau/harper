"""Main server script."""

import uvicorn
from fastapi import FastAPI, HTTPException

import harper.workflow as workflow
from harper.util import HarperExc

app = FastAPI()


@app.get("/")
async def root():
    """Home page."""
    return {"message": "Hello Harper"}


@app.get("/lessons")
async def get_all_lessons():
    """List of most recent versions of all lessons."""
    try:
        return workflow.get_all_lessons()
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)


@app.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id, sequence_id=None):
    """A specific (version of a) lesson."""
    try:
        return workflow.get_lesson(lesson_id, sequence_id)
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)


@app.get("/person/{person_id}")
async def get_person(person_id):
    """A person."""
    try:
        return workflow.get_person(person_id)
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.server:app", host="0.0.0.0", port=80, reload=True)
