from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.poll import PollModel, PollOptionModel
from app.domain.poll import Poll, PollCreate


class PollRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[Poll]:
        result = await self.session.execute(
            select(PollModel).options(selectinload(PollModel.options))
        )

        polls = result.scalars().all()
        return [Poll.model_validate(p) for p in polls]

    async def create(self, create: PollCreate) -> Poll:
        db_poll = PollModel(**create.model_dump(exclude={"options"}))
        for option_create in create.options:
            db_option = PollOptionModel(**option_create.model_dump())
            db_poll.options.append(db_option)

        self.session.add(db_poll)

        await self.session.commit()
        await self.session.refresh(db_poll, attribute_names=["options"])

        return Poll.model_validate(db_poll)

    async def get(self, poll_id: int) -> Poll | None:
        result = await self.session.execute(
            select(PollModel)
            .options(selectinload(PollModel.options))
            .where(PollModel.id == poll_id)
        )
        db_poll = result.scalar_one()
        return Poll.model_validate(db_poll)
