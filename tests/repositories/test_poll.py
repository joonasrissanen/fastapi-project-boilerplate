import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.poll import PollRepository
from app.domain.poll import PollCreate, PollOptionCreate

pytestmark = pytest.mark.anyio


async def test_create(async_session: AsyncSession):
    repository = PollRepository(async_session)
    create = PollCreate(
        question="What is the best color?",
        options=[PollOptionCreate(text=text) for text in ["Red", "Blue", "Green"]],
    )
    created = await repository.create(create)

    assert created.id is not None
    assert created.question == create.question

    poll = await repository.get(created.id)

    assert poll is not None
    assert poll.id == created.id
    assert len(poll.options) == len(create.options)
    for option, option_create in zip(poll.options, create.options):
        assert option.text == option_create.text


async def test_get(async_session: AsyncSession):
    repository = PollRepository(async_session)
    create = PollCreate(
        question="What is the best color?",
        options=[PollOptionCreate(text=text) for text in ["Red", "Blue", "Green"]],
    )
    created = await repository.create(create)

    poll = await repository.get(created.id)

    assert poll is not None
    assert poll.id == created.id
    assert poll.question == create.question
    assert len(poll.options) == len(create.options)
    for option, option_create in zip(poll.options, create.options):
        assert option.text == option_create.text


async def test_list(async_session: AsyncSession):
    repository = PollRepository(async_session)
    create1 = PollCreate(
        question="What is the best color?",
        options=[PollOptionCreate(text=text) for text in ["Red", "Blue", "Green"]],
    )
    create2 = PollCreate(
        question="What is the best animal?",
        options=[PollOptionCreate(text=text) for text in ["Dog", "Cat", "Bird"]],
    )
    await repository.create(create1)
    await repository.create(create2)

    polls = await repository.list()

    assert len(polls) == 2
    questions = [poll.question for poll in polls]
    assert create1.question in questions
    assert create2.question in questions
