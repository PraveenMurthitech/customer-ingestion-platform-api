from pydantic import BaseModel
from typing import Any


class StandardResponse(BaseModel):
    status: str
    status_code: int
    data: Any
    message: str