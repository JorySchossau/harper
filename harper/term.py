from fastapi import APIRouter, HTTPException

import harper.workflow as workflow
from harper.util import HarperExc


router = APIRouter()


@router.get("/all/")
async def get_all_terms():
    """All terms with frequency count."""
    try:
        return workflow.get_all_terms()
    except HarperExc as exc:
        raise HTTPException(status_code=exc.code, detail=exc.message)
