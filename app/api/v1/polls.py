from fastapi import APIRouter, Body, Depends, status

from app.dependencies.polls import get_poll_service
from app.domain.poll import Poll, PollCreate
from app.services.poll import PollService

router = APIRouter(tags=["polls"])


@router.post(
    path="/polls",
    response_model=Poll,
    status_code=status.HTTP_201_CREATED,
)
async def create_poll(
    create: PollCreate = Body(...),
    poll_service: PollService = Depends(get_poll_service),
):
    return await poll_service.create(create)


@router.get(
    path="/polls",
    response_model=list[Poll],
    status_code=status.HTTP_200_OK,
)
async def list_polls(poll_service: PollService = Depends(get_poll_service)):
    return await poll_service.list()


@router.get(
    path="/polls/{poll_id}",
    response_model=Poll,
    status_code=status.HTTP_200_OK,
)
async def get_poll(
    poll_id: int,
    poll_service: PollService = Depends(get_poll_service),
):
    return await poll_service.get(poll_id)
