from pydantic import BaseModel

from .request import Request
from .response import Response


# TODO: contract as dict or as basemodel
class Contract(BaseModel):
    producer: str
    consumer: str
    contract: dict
    request: Request
    response: Response

    class Config(object):
        orm_mode = True
