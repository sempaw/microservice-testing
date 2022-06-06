from .base_repository import BaseRepository
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate


class ContractRepository(BaseRepository[Contract, ContractCreate, ContractUpdate]):
    ...


contract = ContractRepository(Contract)

# import logging
# from typing import Optional, List
# from fastapi import HTTPException
#
# from app.exceptions.not_found_exception import NotFoundException
# from app.schemas.contract import Contract

# logger = logging.getLogger(__name__)
# _contracts: List[Contract] = []
#
#
# def get_all() -> List[Contract]:
#     return _contracts
#
#
# def get_by_id(contract_id: id) -> Optional[Contract]:
#     for ctc in _contracts:
#         if ctc.id == contract_id:
#             return ctc
#     raise HTTPException(
#         status_code=404,
#         detail=f"Contract with given id: {contract_id} has not been found"
#     )
#
#
# def create(contract: Contract) -> id:
#     ctc_id = len(_contracts)
#     contract.id = ctc_id
#     _contracts.append(contract)
#     return contract.id
#
#
# def update(contract_id: id, contract: Contract) -> None:
#     for ctc in _contracts:
#         if ctc.id == contract_id:
#             ctc = contract
#             return
#     raise NotFoundException(f"Contract with given id: {contract_id} has not been found")
#
#
# def delete(contract_id: id) -> None:
#     for ctc in _contracts:
#         if ctc.id == contract_id:
#             _contracts.remove(ctc)
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f"Contract with given id: {contract_id} has not been found"
#     )
