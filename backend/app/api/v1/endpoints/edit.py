from fastapi import APIRouter, Depends

from app.api.deps import get_agent_service
from app.models.schemas import ApplyEditRequest

router = APIRouter()


@router.post("/apply-edit")
async def apply_edit(
    request: ApplyEditRequest,
    agent_service=Depends(get_agent_service),
):
    return agent_service.apply_edit(request.edit_id)