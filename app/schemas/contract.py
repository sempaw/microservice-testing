from typing import Optional
from pydantic import BaseModel


class ContractBase(BaseModel):
    token: str
    data: dict


class ContractCreate(ContractBase):
    ...


class ContractUpdate(ContractBase):
    ...


class ContractInDBBase(ContractBase):
    id: Optional[int] = None
    consumer_id: Optional[int] = None
    spec_id: Optional[int] = None

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass

