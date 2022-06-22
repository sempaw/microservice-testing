from datetime import datetime, timedelta
from typing import List, MutableMapping, Optional, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.core.settings import settings
from app.models.user import User
from app.repositories.user_repository_async import UserRepositoryAsync, user_repo_async


JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
user_repo: UserRepositoryAsync = user_repo_async


async def authenticate(
    *,
    login: str,
    password: str,
    db: AsyncSession,
) -> Optional[User]:
    user = await user_repo.get_by_login(db=db, login=login)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire  # type: ignore
    payload["iat"] = datetime.utcnow()  # type: ignore
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
