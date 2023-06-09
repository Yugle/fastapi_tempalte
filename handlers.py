from fastapi import status
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas.base import ErrorResponseBody, HTTPException


def http_exception_handler(_, e: StarletteHTTPException):
    logger.error(e)

    return JSONResponse(
        status_code=e.status_code,
        content=ErrorResponseBody(e.status_code, e.detail).__dict__,
        headers=e.headers
    )


def custom_http_exception_handler(_, e: HTTPException):
    logger.error(e)

    return JSONResponse(
        status_code=e.status_code,
        content=ErrorResponseBody(e.status_code, e.message).__dict__,
        headers=e.headers
    )


async def validation_exception_handler(_, e: RequestValidationError):
    logger.error(e)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponseBody(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(e)).__dict__
    )
