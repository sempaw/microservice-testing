import logging
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException

from app.schemas.contract import Contract

# TODO: перелопатить все нафиг
# TODO: logging
# TODO: replace static with async
logger = logging.getLogger(__name__)
_contracts: List[Contract] = []


def get_all() -> List[Contract]:
    return _contracts


def get_by_id(contract_id: UUID) -> Optional[Contract]:
    for ctc in _contracts:
        if ctc.id == contract_id:
            return ctc
    raise HTTPException(
        status_code=404,
        detail=f"Contract with given id: {contract_id} has not been found"
    )


def create(contract: Contract) -> UUID:
    # TODO: check if contract already exists
    _contracts.append(contract)
    return contract.id


def update(contract_id: UUID, request: Contract) -> None:
    contract_update = request.contract
    for ctc in _contracts:
        # TODO: Nested updates
        # marshmallow
        if ctc.id == contract_id:
            if contract_update.producer:
                ctc.producer = contract_update.producer
            if contract_update.consumer:
                ctc.consumer = contract_update.consumer
            if contract_update.url:
                ctc.url = contract_update.url
            if contract_update.request:
                ctc.request = contract_update.request
            if contract_update.response:
                ctc.response = contract_update.response
            return
    # TODO: what kind of exceptions?
    raise HTTPException(
        status_code=404,
        detail=f"Contract with given id: {contract_id} has not been found"
    )


def delete(contract_id: UUID) -> None:
    for ctc in _contracts:
        if ctc.id == contract_id:
            _contracts.remove(ctc)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Contract with given id: {contract_id} has not been found"
    )
