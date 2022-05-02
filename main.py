import logging
from typing import List
from uuid import UUID
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse
from app.core.auth import Auth
from app.core.contract_validator import ContractValidator

from app.repositories.contract import DB
from app.schemas.contract import Contract
from app.core.token import Token

from app.api.api_v1 import api

app = FastAPI()
app.include_router(api.router)


# TODO: move handlers into separate file
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
