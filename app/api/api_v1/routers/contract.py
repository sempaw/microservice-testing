from typing import List
from uuid import UUID
from fastapi import APIRouter, status
import app.core.auth as auth

from app.core.contract_validator import ContractValidator
from app.schemas.contract import Contract
from app.core.token import Token
import app.repositories.contract as contract_repository

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all() -> List[Contract]:
    return contract_repository.get_all()


@router.get("/{contract_id}", status_code=status.HTTP_200_OK)
async def get_by_id(contract_id: UUID) -> Contract:
    return contract_repository.get_by_id(contract_id)


# TODO: does router supports routes only or auth and validation as well?
@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(contract: Contract, token: Token) -> UUID:
    # middleware
    auth.validate_token(token)
    ContractValidator.validate_contract(contract)
    return contract_repository.create(contract)


@router.put('/{contract_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update(contract: Contract, contract_id: UUID):
    contract_repository.update(contract_id, contract)


@router.delete('/{contract_id}')
async def delete(contract_id: UUID):
    contract_repository.delete(contract_id)
