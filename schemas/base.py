from typing import Any, Callable
from bson import ObjectId
from fastapi.types import DecoratedCallable
from fastapi import APIRouter as FastAPIRouter
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, InvalidDiscriminator
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

    def parse_condition_dict(self) -> dict:
        return {key: value for key, value in self.dict().items() if key not in ['page_num', 'limit'] and value}


class ListResultFromDB(Generic[T], BaseModel):
    total: int
    items: List[T]


class APIRouter(FastAPIRouter):
    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        alternate_path = path + "/"
        super().api_route(alternate_path, include_in_schema=False, **kwargs)
        return super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )


class ObjectID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidDiscriminator:
            raise ValueError("Not a valid ObjectId")
