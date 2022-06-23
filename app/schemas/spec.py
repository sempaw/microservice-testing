from typing import Optional

from pydantic import BaseModel


class SpecBase(BaseModel):
    data: dict
    is_deprecated: bool


class SpecCreate(SpecBase):
    data: dict
    provider_id: int
    is_deprecated: bool


class SpecCreateDB(SpecCreate):
    token: str


class SpecUpdate(SpecBase):
    is_deprecated: bool


class SpecInDBBase(SpecBase):
    id: Optional[int] = None
    provider_id: Optional[int] = None
    token: str

    class Config:
        orm_mode = True


class Spec(SpecInDBBase):
    pass
