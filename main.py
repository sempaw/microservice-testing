import logging

from fastapi import FastAPI
import json
from fastapi.responses import JSONResponse

from core.auth import Auth
from core.contract_validator import ContractValidator
from db.session import Session
from models.Contract import Contract
from models.Token import Token

app = FastAPI()
# TODO: logging
logger = logging.getLogger(__name__)


@app.post("/contracts")
async def contracts_post(contract: Contract, token: Token):
    token_validation_result = Auth.validate_token(token)
    if not token_validation_result.success:
        return JSONResponse(status_code=403, content={"message": token_validation_result.value})
    contract_validation_result = ContractValidator.validate_contract(contract)
    if not contract_validation_result.success:
        return JSONResponse(status_code=400, content={"message": contract_validation_result.value})
    contract = Session.save_contract(contract)
    print(contract)
    return JSONResponse(status_code=201, content=json.dumps(contract, default=vars))


# TODO: update
@app.put('/contracts/{id}')
async def contracts_update(contract: Contract, contract_id: int):
    pass


# •	/contracts/{id}/delete/ - удаление контракта
# •	/contracts/{id}/ - просмотр контракта по id
# •	/contracts/ - просмотр всех контрактов
# •	/schemas/upload/ - загрузка схемы
# •	/schemas/{id}/update/ - обновление схемы
# •	/schemas/{id}/delete/ - удаление схемы
# •	/schemas/{id}/deprecated/ - пометка схемы устаревшей
# •	/schemas/{id}/ - просмотр схемы по id
# •	/schemas/ - просмотр всех схем
