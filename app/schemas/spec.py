from typing import Optional

from pydantic import BaseModel


class SpecBase(BaseModel):
    token: str
    data: dict
    is_deprecated: bool


class SpecCreate(SpecBase):
    token: str
    data: dict
    provider_id: int
    is_deprecated: bool


class SpecUpdate(SpecBase):
    is_deprecated: bool


class SpecInDBBase(SpecBase):
    id: Optional[int] = None
    provider_id: Optional[int] = None

    class Config:
        orm_mode = True


class Spec(SpecInDBBase):
    pass
