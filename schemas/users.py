from pydantic import BaseModel
from typing import Optional

from schemas.base import PageQuery


class UserBase(BaseModel):
    username: str
    name: str
    role: int
    company: Optional[str]


class UserToCreate(UserBase):
    password: str


class UserRes(UserBase):
    user_id: int


class UsersQuery(PageQuery):
    role: Optional[int]


class LoginRes(BaseModel):
    user_id: int
    role: int
    access_token: str
    expire_in: int
