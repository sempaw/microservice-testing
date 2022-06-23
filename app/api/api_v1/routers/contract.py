import traceback
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from app.core import deps
from app.exceptions.deprecated_usage_error import DeprecatedUsageError
from app.exceptions.invalid_data_error import InvalidDataError
from app.exceptions.no_access_error import NoAccessError
from app.exceptions.not_found_error import NotFoundError
from app.models.contract import Contract as ContractModel
from app.models.user import User
from app.schemas.contract import ContractCreate
from app.services.contract_service import contract_service
from app.services.user_service import user_service


router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_multi(
    *,
    db=Depends(deps.get_db_async),  # noqa
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> List[ContractModel]:
    """
    Fetch all contracts
    """
    try:
        return await contract_service.get_multi(skip=skip, limit=limit, db=db)
    except NotFoundError as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contract_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    *, db=Depends(deps.get_db_async), contract_id: int  # noqa
) -> Optional[ContractModel]:
    """
    Fetch a single contract by ID
    """
    # service.get
    try:
        return await contract_service.get_by_id(contract_id=contract_id, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(
    *,
    db=Depends(deps.get_db_async),
    user: User = Depends(user_service.get_current_user),
    contract: ContractCreate,
    response: Response,
) -> ContractModel:
    """
    Post new contract
    """
    try:
        return await contract_service.create(contract_create=contract, db=db, user=user)
    except IntegrityError:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail="Integrity error occurred")
    except InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DeprecatedUsageError as e:
        raise HTTPException(status_code=222, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(
    *,
    db=Depends(deps.get_db_async),
    user: User = Depends(user_service.get_current_user),
    contract_id: int,
) -> None:
    """
    Delete contract by ID
    """
    try:
        return await contract_service.remove(contract_id=contract_id, db=db, user=user)
    except NotFoundError as e:
        print(e)
        raise HTTPException(status_code=404, detail=str(e))
    except NoAccessError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contract_id}/depends_on_deprecated", status_code=status.HTTP_200_OK)
async def depends_on_deprecated(
    *, db=Depends(deps.get_db_async), contract_id: int
) -> bool:
    try:
        return await contract_service.depends_on_deprecated(
            db=db, contract_id=contract_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
