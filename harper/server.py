"""Main server script."""

import uvicorn
from fastapi import FastAPI

import harper.lesson
import harper.person
import harper.term

app = FastAPI()


@app.get("/")
async def root():
    """Home page."""
    return {"message": "Hello Harper"}


app.include_router(harper.lesson.router, prefix="/lesson", tags=["Lessons"])
app.include_router(harper.person.router, prefix="/person", tags=["Persons"])
app.include_router(harper.term.router, prefix="/term", tags=["Terms"])


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.server:app", host="0.0.0.0", port=80, reload=True)
