from fastapi import FastAPI
from handlers import http_exception_handler, custom_http_exception_handler, validation_exception_handler
from middlewares import AuthMiddleware, Middleware
from routers import token, users
import uvicorn
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from conf.config import config
from schemas.base import HTTPException

app = FastAPI(exception_handlers={
    StarletteHTTPException: http_exception_handler,
    HTTPException: custom_http_exception_handler,
    RequestValidationError: validation_exception_handler,
})

app.include_router(token.router)
app.include_router(users.router)

app.add_middleware(Middleware)
app.add_middleware(AuthMiddleware)


@app.get("/health")
async def root():
    return {
        "message": "Hello"
    }

if __name__ == '__main__':
    uvicorn.run("main:app", port=int(config.http.port),
                log_level="debug", reload=True)
