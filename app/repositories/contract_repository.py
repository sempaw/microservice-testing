from app.models.contract import Contract
from app.repositories.base_repository import BaseRepository
from app.schemas.contract import ContractCreate, ContractUpdate


class ContractRepository(BaseRepository[Contract, ContractCreate, ContractUpdate]):
    ...


contract = ContractRepository(Contract)
