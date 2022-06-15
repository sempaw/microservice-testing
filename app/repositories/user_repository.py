from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserCreate, UserUpdate]):
    def get_by_login(self, db: Session, *, login: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.login == login).first()

    def update(
        self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser


user = UserRepository(UserModel)
