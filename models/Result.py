from typing import Optional


class Result(object):
    success: Optional[bool]
    value: any

    def __init__(self, success=None, value=None):
        self.success = success
        self.value = value
