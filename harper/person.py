from fastapi import APIRouter, HTTPException

import harper.workflow as workflow
from harper.util import HarperExc


router = APIRouter()


@router.get("/{person_id}/")
async def get_person(person_id):
    """A person."""
    try:
        return workflow.get_person(person_id)
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)
