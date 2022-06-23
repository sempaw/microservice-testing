from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.deprecated_usage_error import DeprecatedUsageError
from app.exceptions.no_access_error import NoAccessError
from app.exceptions.not_found_error import NotFoundError
from app.models.contract import Contract as ContractModel
from app.models.user import User
from app.repositories.contract_repository_async import (
    ContractRepositoryAsync,
    contract_repo_async,
)
from app.repositories.spec_repository_async import SpecRepositoryAsync, spec_repo_async
from app.schemas import ContractCreate
from app.schemas.contract import ContractCreateDB
from app.services.auth_service import auth_service
from app.services.validation_service import validation_service


class ContractService(object):

    _contract_repo: ContractRepositoryAsync = contract_repo_async
    _spec_repo: SpecRepositoryAsync = spec_repo_async

    async def get_by_id(self, db: AsyncSession, contract_id: int) -> ContractModel:
        obj = await self._contract_repo.get(db=db, obj_id=contract_id)
        if obj is None:
            raise NotFoundError("Unable to find contract with given ID")
        return obj

    async def get_multi(
        self, db: AsyncSession, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> List[ContractModel]:
        return await self._contract_repo.get_multi(db=db, skip=skip, limit=limit)

    async def create(
        self, db: AsyncSession, user: User, contract_create: ContractCreate
    ) -> ContractModel:
        await auth_service.confirm_token(user.token)
        await validation_service.validate_contract(data=contract_create.data)
        spec = await self._spec_repo.get(db=db, obj_id=contract_create.spec_id)
        if spec is None:
            raise NotFoundError("Unable to make contract using spec with given ID")
        obj_db_data = dict(jsonable_encoder(contract_create))
        obj_db_data["token"] = user.token
        obj_db = ContractCreateDB(**obj_db_data)
        obj_id = await self._contract_repo.create(db=db, obj_in=obj_db)
        obj = await self._contract_repo.get(db=db, obj_id=obj_id)
        if obj is None:
            raise NotFoundError("Unable to find contract after creating it")
        if spec.is_deprecated:
            raise DeprecatedUsageError(
                f"Contract(ID: {obj_id}) created with usage of deprecated spec"
            )
        return obj

    async def remove(self, db: AsyncSession, user: User, contract_id: int) -> None:
        obj = await self._contract_repo.get(obj_id=contract_id, db=db)
        if obj is None:
            raise NotFoundError("Unable to find contract with given ID")
        if obj.token != user.token or not user.is_superuser:
            raise NoAccessError("No access to remove contract with given ID")
        await self._contract_repo.remove(obj_id=contract_id, db=db)


contract_service = ContractService()
