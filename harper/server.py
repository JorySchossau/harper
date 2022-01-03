"""Main server script."""

import argparse
import sys

import uvicorn
from fastapi import FastAPI

import harper.lesson
import harper.person
import harper.term
from harper.db import DB
from harper.util import HarperExc

app = FastAPI()


@app.on_event("startup")
def initialize():
    """Register an event handler that's called when the application restarts.

    We need this because FastAPI may dynamically reload code, but every time it
    does we lose any class-level initialization we've done.

    <https://stackoverflow.com/questions/68769839/re-running-an-initialization-function-for-each-api-reload>
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--db", default="test", help="Database connection string.")
    config = parser.parse_args()
    DB.configure(config.db)


@app.get("/")
async def root():
    """Home page."""
    return {"message": "Hello Harper"}


app.include_router(harper.lesson.router, prefix="/lesson", tags=["Lessons"])
app.include_router(harper.person.router, prefix="/person", tags=["Persons"])
app.include_router(harper.term.router, prefix="/term", tags=["Terms"])


if __name__ == "__main__":
    try:
        uvicorn.run("harper.server:app", host="0.0.0.0", port=80, reload=True)
    except HarperExc as exc:
        print(exc.message, file=sys.stderr)
        sys.exit(1)
