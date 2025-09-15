from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.poll import PollRepository
from app.dependencies.database import get_database
from app.services.poll import PollService


def get_poll_repository(
    session: AsyncSession = Depends(get_database),
) -> PollRepository:
    return PollRepository(session)


def get_poll_service(
    repository: PollRepository = Depends(get_poll_repository),
) -> PollService:
    return PollService(repository)
