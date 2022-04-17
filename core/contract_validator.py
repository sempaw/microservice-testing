from models.Contract import Contract
from models.Result import Result


class ContractValidator(object):
    class Responses(object):
        OK = "OK"
        CONTRACT_IS_NOT_GIVEN = "Contract has not been given"
        PRODUCER_IS_NOT_GIVEN = "Producer ID has not been given"
        CONSUMER_IS_NOT_GIVEN = "Consumer ID has not been given"

    @classmethod
    def validate_contract(cls, contract: Contract) -> Result:
        result = Result()
        if not contract:
            result.success = False
            result.value = cls.Responses.CONTRACT_IS_NOT_GIVEN
            return result
        if not contract.producer:
            result.success = False
            result.value = cls.Responses.PRODUCER_IS_NOT_GIVEN
            return result
        if not contract.consumer:
            result.success = False
            result.value = cls.Responses.CONSUMER_IS_NOT_GIVEN
            return result
        result.success = True
        result.value = cls.Responses.OK
        return result
