from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


T = TypeVar("T")


class HTTPException(StarletteHTTPException):
    def __init__(self, status_code: int, message: str, headers: Optional[dict] = None,):
        self.status_code = status_code
        self.message = message
        self.headers = headers


class ErrorResponseBody:
    def __init__(self, status_code, message):
        self.status = status_code
        self.message = message


class ListResponseBody(Generic[T], BaseModel):
    items: List[T]
    page_num: int
    limit: int
    total: int


class PageQuery(BaseModel):
    page_num: int
    limit: int


class ListResultFromDB(Generic[T], BaseModel):
    total: int
    items: List[T]
