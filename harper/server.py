"""Main server script."""

import uvicorn
from fastapi import FastAPI, HTTPException

import harper.workflow as workflow
from harper.util import HarperExc

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Harper"}


@app.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id, sequence_id=None):
    try:
        return workflow.get_lesson(lesson_id, sequence_id)
    except HarperExc as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@app.get("/person/{person_id}")
async def get_person(person_id):
    try:
        return workflow.get_person(person_id)
    except HarperExc as exc:
        raise HTTPException(status_code=404, detail=exc.message)


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.server:app", host="0.0.0.0", port=80, reload=True)
