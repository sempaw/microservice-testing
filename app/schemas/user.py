from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    token: str
    is_superuser: bool = False


class UserCreate(UserBase):
    login: str
    password: str
    token: str


class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    password: str


class User(UserInDBBase):
    ...
