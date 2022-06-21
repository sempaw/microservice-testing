from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.contract_validator import validate_contract
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException
from app.models.contract import Contract as ContractModel
from app.schemas.contract import ContractCreate, ContractUpdate
from app.services.contract_service import ContractService


router = APIRouter(prefix="/contracts", tags=["contracts"])
contract_service: ContractService = ContractService()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_multi(
    *,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> List[ContractModel]:
    """
    Fetch all contracts
    """
    try:
        return await contract_service.get_multi(db=db, skip=skip, limit=limit)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contract_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    *, contract_id: int, db: AsyncSession = Depends(deps.get_db_async)  # noqa
) -> Optional[ContractModel]:
    """
    Fetch a single contract by ID
    """
    # service.get
    try:
        return await contract_service.get_by_id(contract_id=contract_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(
    *, contract: ContractCreate, db: AsyncSession = Depends(deps.get_db_async)  # noqa
) -> ContractModel:
    """
    Post new contract
    """
    try:
        validate_contract(data=contract.data)
        return await contract_service.create(contract_create=contract, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{contract_id}", status_code=status.HTTP_200_OK)
async def update(
    *,
    contract: ContractUpdate,
    contract_id: int,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> ContractModel:
    """
    Update whole contract by ID
    """
    try:
        validate_contract(contract.data)
        return await contract_service.update(
            contract_id=contract_id, contract_update=contract, db=db
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{contract_id}", status_code=status.HTTP_200_OK)
async def remove(
    *,
    contract_id: int,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
):
    """
    Delete contract by ID
    """
    try:
        return await contract_service.remove(contract_id=contract_id, db=db)
    except NotFoundException as e:
        print(e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
