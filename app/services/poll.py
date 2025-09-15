from app.db.repositories.poll import PollRepository
from app.domain.poll import Poll, PollCreate
from app.exceptions import NotFoundError


class PollService:
    def __init__(self, repository: PollRepository):
        self.repository = repository

    async def list(self) -> list[Poll]:
        polls = await self.repository.list()
        return polls

    async def create(self, create: PollCreate) -> Poll:
        poll = await self.repository.create(create)
        return poll

    async def get(self, poll_id: int) -> Poll:
        poll = await self.repository.get(poll_id)
        if not poll:
            raise NotFoundError(entity_name="Poll", identifier=str(poll_id))
        return poll
