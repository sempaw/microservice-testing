from typing import Any, Dict, Union

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.repositories.base_repository_async import BaseRepositoryAsync
from app.schemas.user import UserCreate, UserUpdate


class UserRepositoryAsync(BaseRepositoryAsync[UserModel, UserCreate, UserUpdate]):
    async def get_by_login(
        self,
        login: str,
        db: AsyncSession,
    ) -> UserModel:
        stmt = select(self.model).where(UserModel.login == login)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        return obj

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> int:
        create_data = obj_in.dict()
        create_data.pop("password")
        create_data["password"] = get_password_hash(obj_in.password)
        stmt = insert(self.model).values(create_data)
        result = await db.execute(stmt)
        await db.commit()
        obj_id = result.inserted_primary_key[0]
        return obj_id

    async def update(
        self, db: AsyncSession, obj_id: int, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> None:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        await super().update(db, obj_id=obj_id, obj_in=update_data)


user_repo_async = UserRepositoryAsync(UserModel)
