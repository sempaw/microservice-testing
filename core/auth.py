from enum import Enum
from typing import Optional

from models.Token import Token
from models.Result import Result


class Auth(object):
    tokens = ['', 'test', 'admin', 'token']

    class Responses(object):
        OK = "OK"
        NOT_AUTHENTICATED = "Not authenticated request"
        INVALID_TOKEN = "Provided token is invalid"
        EXPIRED_TOKEN = "Provided token has been expired"

    @classmethod
    def validate_token(cls, token: Token) -> Result:
        result = Result()
        if not token:
            result.success = False
            result.value = cls.Responses.NOT_AUTHENTICATED
            return result
        # TODO: expires in
        result.success = True
        result.value = cls.Responses.OK
        return result
