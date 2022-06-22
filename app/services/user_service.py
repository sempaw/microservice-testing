from fastapi import Depends
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.auth import oauth2_scheme
from app.core.settings import settings
from app.exceptions.already_exists_error import AlreadyExistsError
from app.exceptions.credentials_error import CredentialsError
from app.exceptions.not_found_error import NotFoundError
from app.models.user import User
from app.models.user import User as UserModel
from app.repositories.user_repository_async import UserRepositoryAsync, user_repo_async
from app.schemas import UserCreate


class UserService(object):

    _user_repo: UserRepositoryAsync = user_repo_async

    async def create(self, db: AsyncSession, user_create: UserCreate) -> UserModel:
        user = await self._user_repo.get_by_login(user_create.login, db=db)
        if user:
            raise AlreadyExistsError("User with given login already exists")
        obj_id = await self._user_repo.create(db=db, obj_in=user_create)
        new_user = await self._user_repo.get(obj_id=obj_id, db=db)
        if new_user is None:
            raise NotFoundError("Unable to find user after creating it")
        return new_user

    async def get_current_user(
        self,
        db: AsyncSession = Depends(deps.get_db_async),  # noqa
        token: str = Depends(oauth2_scheme),  # noqa
    ) -> User:
        class TokenData(BaseModel):
            username: str

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.ALGORITHM],
                options={"verify_aud": False},
            )
            username: str = payload.get("sub")
            token_data = TokenData(username=username)
        except JWTError:
            raise CredentialsError("")
        user = await user_repo_async.get_by_login(login=token_data.username, db=db)
        if user is None:
            raise CredentialsError("")
        return user


user_service = UserService()
