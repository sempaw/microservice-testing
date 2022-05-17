from typing import List
from fastapi import APIRouter, status, HTTPException

from app.core.contract_validator import ContractValidator
from app.schemas.contract import Contract
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException
import app.repositories.contracts_repository as contract_repository


router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all() -> List[Contract]:
    """
    Fetch all contracts
    """

    return contract_repository.get_all()



@router.get("/{contract_id}", status_code=status.HTTP_200_OK)
async def get_by_id(contract_id: int) -> Contract:
    """
    Fetch a single contract by ID
    """

    return contract_repository.get_by_id(contract_id)


# TODO: does router supports routes only or auth and validation as well?
@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(contract: Contract) -> int:
    """
    Post new contract
    """

    try:
        ContractValidator.validate_contract(contract.data)
        contract_repository.create(contract)
        return contract_repository.create(contract)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{contract_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update(contract: Contract, contract_id: int):
    """
    Update whole contract by ID
    """

    try:
        ContractValidator.validate_contract(contract.data)
        contract_repository.update(contract_id, contract)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{contract_id}')
async def delete(contract_id: int):
    """
    Delete contract by ID
    """

    contract_repository.delete(contract_id)
