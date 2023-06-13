from pydantic import BaseModel
from typing import Optional

from schemas.base import PageQuery


class UserBase(BaseModel):
    nt_account: str
    email: str
    department: str
    name: str
    role: int


class User(UserBase):
    user_id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class UsersQuery(PageQuery):
    role: Optional[int]
    email: Optional[str]


class LoginRes(BaseModel):
    user_id: int
    role: int
    access_token: str
    expire_in: int
