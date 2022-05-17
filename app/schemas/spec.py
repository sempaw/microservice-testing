from typing import Optional
from pydantic import BaseModel


class SpecBase(BaseModel):
    token: str
    data: dict


class SpecCreate(SpecBase):
    ...


class SpecUpdate(SpecBase):
    ...


class SpecInDBBase(SpecBase):
    id: Optional[int] = None
    provider_id: Optional[int] = None

    class Config:
        orm_mode = True


class Spec(SpecInDBBase):
    pass
