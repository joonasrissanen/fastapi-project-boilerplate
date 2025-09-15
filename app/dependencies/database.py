from app.db.database import sessionmanager


async def get_database():
    async with sessionmanager.session() as session:
        yield session
