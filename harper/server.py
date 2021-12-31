"""Main server script."""

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Harper"}


# Run from the command line.
if __name__ == "__main__":
    uvicorn.run("harper.main:app", host="0.0.0.0", port=80, reload=True)
