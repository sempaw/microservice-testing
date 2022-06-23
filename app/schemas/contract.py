from typing import Optional

from pydantic import BaseModel


class ContractBase(BaseModel):
    data: dict


class ContractCreate(ContractBase):
    data: dict
    consumer_id: int
    spec_id: int


class ContractCreateDB(ContractCreate):
    token: str


class ContractUpdate(ContractBase):
    ...


class ContractInDBBase(ContractBase):
    id: Optional[int] = None
    consumer_id: Optional[int] = None
    spec_id: Optional[int] = None
    token: str

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass
