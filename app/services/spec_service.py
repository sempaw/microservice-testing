from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.no_access_error import NoAccessError
from app.exceptions.not_found_error import NotFoundError
from app.models.spec import Spec as SpecModel
from app.models.user import User
from app.repositories.spec_repository_async import SpecRepositoryAsync, spec_repo_async
from app.schemas import SpecCreate
from app.schemas.spec import SpecCreateDB, SpecUpdate
from app.services.auth_service import auth_service
from app.services.validation_service import validation_service


class SpecService(object):

    _spec_repo: SpecRepositoryAsync = spec_repo_async

    async def get_by_id(self, db: AsyncSession, spec_id) -> SpecModel:
        obj = await self._spec_repo.get(db=db, obj_id=spec_id)
        if obj is None:
            raise NotFoundError("Unable to find spec with given ID")
        return obj

    async def get_multi(
        self, db: AsyncSession, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> List[SpecModel]:
        return await self._spec_repo.get_multi(db=db, skip=skip, limit=limit)

    async def create(
        self, db: AsyncSession, user: User, spec_create: SpecCreate
    ) -> SpecModel:
        await auth_service.confirm_token(user.token)
        await validation_service.validate_spec(data=spec_create.data)
        obj_db_data = dict(jsonable_encoder(spec_create))
        obj_db_data["token"] = user.token
        obj_db = SpecCreateDB(**obj_db_data)
        obj_id = await self._spec_repo.create(db=db, obj_in=obj_db)
        obj = await self._spec_repo.get(obj_id=obj_id, db=db)
        if obj is None:
            raise NotFoundError("Unable to find spec after creating it")
        return obj

    async def update(
        self, db: AsyncSession, spec_update: SpecUpdate, spec_id: int
    ) -> None:
        obj = await self._spec_repo.get(obj_id=spec_id, db=db)
        if obj is None:
            raise NotFoundError("Unable to find spec with given ID")
        await validation_service.validate_spec(data=spec_update.data)
        await self._spec_repo.update(db=db, obj_in=spec_update, obj_id=spec_id)

    async def remove(self, db: AsyncSession, user: User, spec_id: int) -> None:
        obj = await self._spec_repo.get(obj_id=spec_id, db=db)
        if obj is None:
            raise NotFoundError("Unable to find spec with given ID")
        if obj.token != user.token or not user.is_superuser:
            raise NoAccessError("No access to remove spec with given ID")
        await self._spec_repo.remove(obj_id=spec_id, db=db)

    async def mark_deprecated(
        self, db: AsyncSession, user: User, spec_id: int, is_deprecated: bool
    ) -> None:
        obj = await self._spec_repo.get(obj_id=spec_id, db=db)
        if obj is None:
            raise NotFoundError("Unable to find spec with given ID")
        if obj.token != user.token or not user.is_superuser:
            raise NoAccessError(
                "No access to update deprecated property on the spec with given ID"
            )
        obj_in_data = jsonable_encoder(obj)
        spec_update = SpecUpdate(**obj_in_data)
        spec_update.is_deprecated = is_deprecated
        await self._spec_repo.update(db=db, obj_id=spec_id, obj_in=spec_update)


spec_service = SpecService()
