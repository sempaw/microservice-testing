from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.spec_validator import validate_spec
from app.models.spec import Spec as SpecModel
from app.repositories.spec_repository_async import SpecRepositoryAsync, spec
from app.schemas import SpecCreate
from app.schemas.spec import SpecUpdate


class SpecService(object):
    _spec_repo: SpecRepositoryAsync = spec

    async def get_by_id(self, db: AsyncSession, spec_id):
        return await self._spec_repo.get(db=db, obj_id=spec_id)

    async def get_multi(
        self, db: AsyncSession, skip: Optional[int] = None, limit: Optional[int] = None
    ):
        return await self._spec_repo.get_multi(db=db, skip=skip, limit=limit)

    async def create(self, db: AsyncSession, spec_create: SpecCreate):
        validate_spec(data=spec_create.data)
        return await self._spec_repo.create(db=db, obj_in=spec_create)

    async def update(
        self, db: AsyncSession, spec_update: SpecUpdate, spec_id: int
    ) -> SpecModel:
        validate_spec(data=spec_update.data)
        return await self._spec_repo.update(db=db, obj_in=spec_update, obj_id=spec_id)

    async def remove(self, db: AsyncSession, spec_id: int):
        return await self._spec_repo.remove(obj_id=spec_id, db=db)

    async def mark_deprecated(self, db: AsyncSession, spec_id: int, is_deprecated: bool):
        spec_by_id = await self._spec_repo.get(obj_id=spec_id, db=db)
        obj_in_data = jsonable_encoder(spec_by_id)
        spec_update = SpecUpdate(**obj_in_data)
        spec_update.is_deprecated = is_deprecated
        return await self._spec_repo.update(db=db, obj_id=spec_id, obj_in=spec_update)
