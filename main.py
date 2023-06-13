from fastapi import FastAPI
from database.mongo import close_mongo_connection, connect_to_mongo
from handlers import http_exception_handler, custom_http_exception_handler, validation_exception_handler
from middlewares import AuthMiddleware, Middleware
from routers import token, users, login
import uvicorn
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from conf.config import config
from schemas.base import HTTPException

import pydantic
from bson import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI(exception_handlers={
    StarletteHTTPException: http_exception_handler,
    HTTPException: custom_http_exception_handler,
    RequestValidationError: validation_exception_handler,
})

app.include_router(token.router)
app.include_router(users.router)
app.include_router(login.router)

app.add_middleware(Middleware)
app.add_middleware(AuthMiddleware)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.get("/health")
async def root():
    return {
        "message": "Hello"
    }

if __name__ == '__main__':
    uvicorn.run("main:app", port=int(config.http.port),
                log_level="debug", reload=True)
