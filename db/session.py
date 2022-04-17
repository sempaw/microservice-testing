from models.Contract import Contract
from models.Result import Result


class Session(object):
    contracts: [Contract] = []

    # Works both for POST and PUT
    @staticmethod
    def save_contract(contract: Contract) -> Contract:
        # TODO: check if contract already exists
        Session.contracts.append(contract)
        contract.id = len(Session.contracts)
        return contract

    @staticmethod
    def delete_contract(contract_id: int) -> Result:
        pass

    @staticmethod
    def find_contract(contract: Contract) -> bool:
        for ctc in Session.contracts:
            if ctc.id == contract.id:
                return True


