from enum import Enum

from app.schemas.contract import Contract


class ContractValidator(object):
    class Responses(str, Enum):
        ok = "OK"
        contract_is_not_given = "Contract has not been given"
        producer_is_not_given = "Producer ID has not been given"
        consumer_is_not_given = "Consumer ID has not been given"

    @classmethod
    def validate_contract(cls, contract: dict) -> None:
        pass
        # if not contract:
        #     raise ValidationException(cls.Responses.contract_is_not_given)
        # if not contract.producer:
        #     raise ValidationException(cls.Responses.producer_is_not_given)
        # if not contract.consumer:
        #     raise ValidationException(cls.Responses.consumer_is_not_given)
