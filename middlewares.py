from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import (
    BaseHTTPMiddleware, RequestResponseEndpoint)
from fastapi.responses import JSONResponse
from schemas.base import ErrorResponseBody, HTTPException

from utils.utils import getReqPath, verifyToken
from conf.config import config


class Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.debug("Request: " + str(request.__dict__))
        response = await call_next(request)
        logger.debug("Response: " + str(response.__dict__))

        return response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            if getReqPath(request) not in config.ignore_auth_urls:
                authorization = request.headers.get("authorization")
                verifyToken(authorization)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=ErrorResponseBody(e.status_code, e.message).__dict__,
                headers=e.headers
            )

        response = await call_next(request)

        return response
