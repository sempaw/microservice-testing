from fastapi import Depends

from app.repositories.contract_repository import contract


class ContractService(object):
    def get_by_id(self, repository: Depends = contract):
        pass
