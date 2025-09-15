import asyncio
import os

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio.engine import create_async_engine
from testcontainers.postgres import PostgresContainer

from app.dependencies.database import get_database
from app.main import create_app

postgres = PostgresContainer("postgres:17-bullseye")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def engine(request: pytest.Session):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)

    from app.db.database import Base
    from app.db.models import load_all_models

    load_all_models()

    database_url = postgres.get_connection_url(driver="asyncpg")
    os.environ["DATABASE_URL"] = database_url
    engine = create_async_engine(database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(engine: AsyncEngine):
    connection = await engine.connect()
    transaction = await connection.begin()
    async_session = async_scoped_session(
        async_sessionmaker(
            bind=connection,
            autocommit=False,
            expire_on_commit=False,
        ),  # Make sure the settings are the same as in app/db/database.py
        asyncio.current_task,
    )

    async with async_session() as session:
        yield session

        await session.close()
        await transaction.rollback()
        await connection.close()


@pytest.fixture
def app(async_session: AsyncSession):
    app = create_app()
    app.dependency_overrides[get_database] = lambda: async_session
    return app


@pytest.fixture
async def client(
    app: FastAPI,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client
