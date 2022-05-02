from enum import Enum

from fastapi.exceptions import RequestValidationError

from app.core.token import Token


# TODO: move into services/routers + перелопатить все нафиг
# TODO: auth as token or payload
_tokens = ['', 'test', 'admin', 'token']


class Responses(str, Enum):
    OK = "OK"
    NOT_AUTHENTICATED = "Not authenticated request"
    INVALID_TOKEN = "Provided token is invalid"
    EXPIRED_TOKEN = "Provided token has been expired"


# TODO: proper way for auth ensurance
# просто методом запрос в базу
def validate_token(token: Token) -> None:
    if not token:
        raise RequestValidationError(Responses.NOT_AUTHENTICATED)
    if token not in _tokens:
        raise RequestValidationError(Responses.INVALID_TOKEN)
    # TODO: expires in
