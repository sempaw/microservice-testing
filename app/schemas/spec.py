from typing import Optional
from pydantic import BaseModel


class SpecBase(BaseModel):
    token: str
    data: dict


class SpecCreate(SpecBase):
    token: str
    data: dict
    provider_id: int


class SpecUpdate(SpecBase):
    token: str
    data: dict
    provider_id: int


class SpecInDBBase(SpecBase):
    id: Optional[int] = None
    provider_id: Optional[int] = None

    class Config:
        orm_mode = True


class Spec(SpecInDBBase):
    pass
