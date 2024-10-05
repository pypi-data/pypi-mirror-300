from ._base import BaseModel


class BaseResponse(BaseModel):
    code: int
    msg: str
