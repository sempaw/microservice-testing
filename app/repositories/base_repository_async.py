from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.base_class import Base
from app.exceptions.not_found_exception import NotFoundException


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepositoryAsync(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, obj_id: int) -> ModelType:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(stmt)
        obj = result.scal
        if obj is None:
            raise NotFoundException("Unable to find contract with given ID")
        return obj

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: Optional[int] = 0,
        limit: Optional[int] = settings.LIMIT_ENTITIES_DB_QUERY
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = (await db.execute(stmt)).scalars().all()
        return result

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = dict(jsonable_encoder(obj_in))
        stmt = insert(self.model).values(obj_in_data)
        result = await db.execute(stmt)
        await db.commit()
        obj_id = result.inserted_primary_key[0]
        obj = await self.get(db=db, obj_id=obj_id)
        return obj

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in_data = dict(jsonable_encoder(obj_in))
        stmt = update(self.model).values(obj_in_data).where(self.model.id == obj_id)
        await db.execute(stmt)
        await db.commit()
        return await self.get(db=db, obj_id=obj_id)

    async def remove(self, db: AsyncSession, *, obj_id: int) -> ModelType:
        obj = await self.get(db=db, obj_id=obj_id)
        stmt = delete(self.model).where(self.model.id == obj_id)
        await db.execute(stmt)
        await db.commit()
        return obj
