from app.models.contract import Contract
from app.repositories.base_repository_async import BaseRepositoryAsync
from app.schemas.contract import ContractCreate, ContractUpdate


class ContractRepositoryAsync(
    BaseRepositoryAsync[Contract, ContractCreate, ContractUpdate]
):
    ...


contract_repo_async = ContractRepositoryAsync(Contract)
