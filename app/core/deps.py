from typing import AsyncGenerator

from app.db.session_async import async_session


async def get_db_async() -> AsyncGenerator:
    async with async_session() as session:
        yield session
