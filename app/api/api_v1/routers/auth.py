from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.auth import authenticate, create_access_token
from app.exceptions.already_exists_error import AlreadyExistsError
from app.exceptions.credentials_error import CredentialsError
from app.models.user import User as UserModel
from app.schemas import User, UserCreate
from app.services.user_service import user_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = await authenticate(
        login=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(
            login=user.login, is_super_user=user.is_superuser, token=user.token
        ),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    user_create: UserCreate,
    db: AsyncSession = Depends(deps.get_db_async),  # noqa
) -> UserModel:
    """
    Create new user without the need to be logged in.
    """
    try:
        return await user_service.create(user_create=user_create, db=db)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Unique constraint fault")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=User)
async def get_authorized_user(
    user: User = Depends(user_service.get_current_user),  # noqa
) -> User:  # noqa
    """
    Fetch the current logged-in user.
    """
    try:
        cur_user = user
        return cur_user
    except CredentialsError:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
