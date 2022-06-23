from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.exceptions.invalid_data_error import InvalidDataError
from app.exceptions.not_found_error import NotFoundError
from app.models.spec import Spec as SpecModel
from app.schemas import SpecCreate
from app.schemas.spec import SpecUpdate
from app.services.spec_service import spec_service


router = APIRouter(prefix="/specs", tags=["specs"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(
    *,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> List[SpecModel]:
    """
    Fetch all specs
    """
    try:
        return await spec_service.get_multi(skip=skip, limit=limit, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{spec_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    *, spec_id: int, db: AsyncSession = Depends(deps.get_db_async)  # noqa
) -> Optional[SpecModel]:
    """
    Fetch a single spec by ID
    """
    try:
        return await spec_service.get_by_id(spec_id=spec_id, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(
    *, spec: SpecCreate, db: AsyncSession = Depends(deps.get_db_async)  # noqa
) -> SpecModel:
    """
    Post new spec
    """
    try:
        return await spec_service.create(spec_create=spec, db=db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Unique constraint fault")
    except InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{spec_id}", status_code=status.HTTP_200_OK)
async def update(
    *,
    spec: SpecUpdate,
    spec_id: int,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> None:
    """
    Update whole spec by ID
    """
    try:
        await spec_service.update(spec_id=spec_id, spec_update=spec, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Unique constraint fault")
    except InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{spec_id}", status_code=status.HTTP_200_OK)
async def delete(*, spec_id: int, db: AsyncSession = Depends(deps.get_db_async)):  # noqa
    """
    Delete spec by ID
    """
    try:
        return await spec_service.remove(spec_id=spec_id, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{spec_id}/deprecate", status_code=status.HTTP_200_OK)
async def mark_deprecated(
    *,
    spec_id: int,
    is_deprecated: bool,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> None:
    """
    Mark spec by given ID as deprecated
    """
    try:
        await spec_service.mark_deprecated(
            db=db, spec_id=spec_id, is_deprecated=is_deprecated
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
