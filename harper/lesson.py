from fastapi import APIRouter, HTTPException

import harper.workflow as workflow
from harper.util import HarperExc


router = APIRouter()


@router.get("/all/")
async def get_all_lessons():
    """List of most recent versions of all lessons."""
    try:
        return workflow.get_all_lessons()
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)


@router.get("/{lesson_id}/")
async def get_lesson(lesson_id, sequence_id=None):
    """A specific (version of a) lesson."""
    try:
        return workflow.get_lesson(lesson_id, sequence_id)
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)
