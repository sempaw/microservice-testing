from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contract_validator import validate_contract
from app.exceptions.not_found_error import NotFoundError
from app.models.contract import Contract as ContractModel
from app.repositories.contract_repository_async import (
    ContractRepositoryAsync,
    contract_repo_async,
)
from app.repositories.spec_repository_async import SpecRepositoryAsync, spec_repo_async
from app.schemas import ContractCreate
from app.schemas.contract import ContractUpdate


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
        self, db: AsyncSession, contract_create: ContractCreate
    ) -> ContractModel:
        validate_contract(data=contract_create.data)
        obj_id = await self._contract_repo.create(db=db, obj_in=contract_create)
        obj = await self._contract_repo.get(db=db, obj_id=obj_id)
        if obj is None:
            raise NotFoundError("Unable to find contract after creating it")
        return obj

    async def update(
        self, db: AsyncSession, contract_update: ContractUpdate, contract_id: int
    ) -> None:
        validate_contract(data=contract_update.data)
        await self._contract_repo.update(
            db=db, obj_in=contract_update, obj_id=contract_id
        )

    async def remove(self, db: AsyncSession, contract_id: int) -> None:
        await self._contract_repo.remove(obj_id=contract_id, db=db)


contract_service = ContractService()
