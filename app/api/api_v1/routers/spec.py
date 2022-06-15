from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.core.spec_validator import validate_spec
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.validation_exception import ValidationException
from app.models.spec import Spec as SpecModel
from app.repositories.spec_repository import spec as repository
from app.schemas import SpecCreate
from app.schemas.spec import SpecUpdate


router = APIRouter(prefix="/specs", tags=["specs"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(
    *,
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(deps.get_db),
) -> List[SpecModel]:
    """
    Fetch all specs
    """
    try:
        return repository.get_multi(skip=skip, limit=limit, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{spec_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    *, spec_id: int, db: Session = Depends(deps.get_db)
) -> Optional[SpecModel]:
    """
    Fetch a single spec by ID
    """
    try:
        return repository.get(obj_id=spec_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(*, spec: SpecCreate, db: Session = Depends(deps.get_db)) -> SpecModel:
    """
    Post new spec
    """
    try:
        validate_spec(data=spec.data)
        return repository.create(obj_in=spec, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{spec_id}', status_code=status.HTTP_200_OK)
async def update(
    *, spec: SpecUpdate, spec_id: int, db: Session = Depends(deps.get_db)
) -> SpecModel:
    """
    Update whole spec by ID
    """
    try:
        validate_spec(spec.data)
        db_obj = repository.get(db=db, obj_id=spec_id)
        if db_obj is None:
            raise NotFoundException("Unable to find spec with given ID")
        else:
            return repository.update(db_obj=db_obj, obj_in=spec, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{spec_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(*, spec_id: int, db: Session = Depends(deps.get_db)):
    """
    Delete spec by ID
    """
    try:
        repository.remove(obj_id=spec_id, db=db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{spec_id}/deprecate', status_code=status.HTTP_200_OK)
async def mark_deprecated(*, spec_id: int, db: Session = Depends(deps.get_db)):
    """
    Mark spec by given ID as deprecated
    """
    try:
        spec = repository.get(obj_id=spec_id, db=db)
        if spec is None:
            raise NotFoundException("Unable to find spec with given ID")
        else:
            spec.is_deprecated = True
            return spec
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
