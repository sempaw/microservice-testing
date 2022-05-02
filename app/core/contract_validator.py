from enum import Enum
from fastapi.exceptions import RequestValidationError

from app.schemas.contract import Contract


class ContractValidator(object):
    class Responses(str, Enum):
        ok = "OK"
        contract_is_not_given = "Contract has not been given"
        producer_is_not_given = "Producer ID has not been given"
        consumer_is_not_given = "Consumer ID has not been given"

    @classmethod
    def validate_contract(cls, contract: Contract) -> None:
        if not contract:
            raise RequestValidationError(cls.Responses.contract_is_not_given)
        if not contract.producer:
            raise RequestValidationError(cls.Responses.producer_is_not_given)
        if not contract.consumer:
            raise RequestValidationError(cls.Responses.consumer_is_not_given)
