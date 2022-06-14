from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core import deps
from app.core.contract_validator import validate_contract
from app.schemas.contract import Contract, ContractUpdate, ContractCreate
from app.models.contract import Contract as ContractModel
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException
from app.repositories.contracts_repository import contract as repository


router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(
        *,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(deps.get_db),
) -> List[Contract]:
    """
    Fetch all contracts
    """
    try:
        return repository.get_multi(skip=skip, limit=limit, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contract_id}", status_code=status.HTTP_200_OK)
async def get_by_id(*, contract_id: int, db: Session = Depends(deps.get_db)) -> Contract:
    """
    Fetch a single contract by ID
    """
    # service.get
    try:
        return repository.get(obj_id=contract_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(*, contract: ContractCreate, db: Session = Depends(deps.get_db)) -> ContractModel:
    """
    Post new contract
    """
    try:
        validate_contract(data=contract.data)
        return repository.create(obj_in=contract, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{contract_id}', status_code=status.HTTP_200_OK)
async def update(*, contract: ContractUpdate, contract_id: int, db: Session = Depends(deps.get_db)) -> ContractModel:
    """
    Update whole contract by ID
    """
    try:
        validate_contract(contract.data)
        db_obj = repository.get(db=db, obj_id=contract_id)
        return repository.update(db_obj=db_obj, obj_in=contract, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{contract_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(*, contract_id: int, db: Session = Depends(deps.get_db)):
    """
    Delete contract by ID
    """
    try:
        repository.remove(obj_id=contract_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
