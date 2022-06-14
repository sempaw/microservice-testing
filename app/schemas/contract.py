from typing import Optional
from pydantic import BaseModel


class ContractBase(BaseModel):
    token: str
    data: dict


class ContractCreate(ContractBase):
    token: str
    data: dict
    consumer_id: int
    spec_id: int


class ContractUpdate(ContractBase):
    token: str
    data: dict


class ContractInDBBase(ContractBase):
    id: Optional[int] = None
    consumer_id: Optional[int] = None
    spec_id: Optional[int] = None

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass
