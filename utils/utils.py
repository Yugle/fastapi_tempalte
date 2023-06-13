from datetime import datetime, timedelta
from typing import Optional

from conf.config import config
from jose import JWTError, jwt
from fastapi import Request, status
from passlib.context import CryptContext

from schemas.base import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = int((datetime.utcnow() +
                 timedelta(minutes=int(config.jwt.access_token_expire_minutes))).timestamp())
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.jwt.secret_key, algorithm=config.jwt.algorithm)

    return [encoded_jwt, expire]


def decodeToken(token: str):
    try:
        return jwt.decode(token, config.jwt.secret_key, config.jwt.algorithm)
    except JWTError:
        return None


def verifyToken(token: Optional[str]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    payload = decodeToken(token)
    if payload is None:
        raise credentials_exception
    nt_account: str = payload.get("sub")
    if nt_account is None:
        raise credentials_exception

    return payload


def getReqPath(request: Request) -> str:
    path = request.scope.get("path")
    if path.endswith('/'):
        path = path[:-1]

    return path
