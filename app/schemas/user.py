from typing import Optional
from pydantic import BaseModel, SecretStr


class UserBase(BaseModel):
    login: Optional[str]
    password: Optional[SecretStr]
    token: Optional[str] = None
    is_superuser: bool = False


class UserCreate(UserBase):
    login: str
    password: SecretStr
    token: str


class UserUpdate(UserBase):
    login: str
    password: SecretStr
    token: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass
