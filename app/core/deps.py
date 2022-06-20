from typing import AsyncGenerator, Generator

from app.db.session import SessionLocal
from app.db.session_async import async_session


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_db_async() -> AsyncGenerator:
    async with async_session() as session:
        yield session
