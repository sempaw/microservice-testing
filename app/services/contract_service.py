from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contract_validator import validate_contract
from app.models.contract import Contract as ContractModel
from app.repositories.contract_repository_async import ContractRepositoryAsync, contract
from app.repositories.spec_repository_async import SpecRepositoryAsync, spec
from app.schemas import ContractCreate
from app.schemas.contract import ContractUpdate


class ContractService(object):
    _contract_repo: ContractRepositoryAsync = contract
    _spec_repo: SpecRepositoryAsync = spec

    async def get_by_id(self, db: AsyncSession, contract_id: int):
        return await self._contract_repo.get(db=db, obj_id=contract_id)

    async def get_multi(
        self, db: AsyncSession, skip: Optional[int] = None, limit: Optional[int] = None
    ):
        return await self._contract_repo.get_multi(db=db, skip=skip, limit=limit)

    async def create(self, db: AsyncSession, contract_create: ContractCreate):
        validate_contract(data=contract_create.data)
        return await self._contract_repo.create(db=db, obj_in=contract_create)

    async def update(
        self, db: AsyncSession, contract_update: ContractUpdate, contract_id: int
    ) -> ContractModel:
        validate_contract(data=contract_update.data)
        return await self._contract_repo.update(
            db=db, obj_in=contract_update, obj_id=contract_id
        )

    async def remove(self, db: AsyncSession, contract_id: int):
        return await self._contract_repo.remove(obj_id=contract_id, db=db)
