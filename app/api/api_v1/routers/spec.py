from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.spec_validator import validate_spec
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException
from app.models.spec import Spec as SpecModel
from app.repositories.spec_repository_async import spec as repository
from app.schemas import SpecCreate
from app.schemas.spec import SpecUpdate


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
        return await repository.get_multi(skip=skip, limit=limit, db=db)
    except NotFoundException as e:
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
        return await repository.get(obj_id=spec_id, db=db)
    except NotFoundException as e:
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
        validate_spec(data=spec.data)
        return await repository.create(obj_in=spec, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{spec_id}", status_code=status.HTTP_200_OK)
async def update(
    *,
    spec: SpecUpdate,
    spec_id: int,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> SpecModel:
    """
    Update whole spec by ID
    """
    try:
        validate_spec(spec.data)
        return await repository.update(obj_id=spec_id, obj_in=spec, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{spec_id}", status_code=status.HTTP_200_OK)
async def delete(*, spec_id: int, db: AsyncSession = Depends(deps.get_db_async)):  # noqa
    """
    Delete spec by ID
    """
    try:
        return await repository.remove(obj_id=spec_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{spec_id}/deprecate", status_code=status.HTTP_200_OK)
async def mark_deprecated(
    *,
    spec_id: int,
    is_deprecated: bool,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> SpecModel:
    """
    Mark spec by given ID as deprecated
    """
    try:
        # TODO: make it right way
        spec = await repository.get(obj_id=spec_id, db=db)
        spec_update = SpecUpdate()
        spec_update.data = spec.data
        spec_update.token = spec.token
        spec_update.is_deprecated = is_deprecated
        return await repository.update(db=db, obj_id=spec_id, obj_in=spec_update)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
