from fastapi import Depends

from app.repositories.contracts_repository import contract


class ContractService(object):
    def get_by_id(self, repository: Depends = contract):
        pass
