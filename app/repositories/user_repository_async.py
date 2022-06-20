from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.models.user import User as UserModel
from app.repositories.base_repository_async import BaseRepositoryAsync
from app.schemas.user import UserCreate, UserUpdate


class UserRepositoryAsync(BaseRepositoryAsync[UserModel, UserCreate, UserUpdate]):
    async def get_by_login(
        self, async_session: sessionmaker, *, login: str
    ) -> Optional[UserModel]:
        with async_session() as db:
            stmt = select(UserModel).where(UserModel.login == login)
            result = await db.execute(stmt)
            return result.scalars().first()


user = UserRepositoryAsync(UserModel)
