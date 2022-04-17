from pydantic import BaseModel

from models.Response import Response
from models.Request import Request


class Contract(BaseModel):
    id: int = None
    producer: str
    consumer: str
    url: str
    request: Request
    response: Response
