from fastapi import APIRouter, Depends, Body, status
from database.sql_server import get_db
from dao.users import *
from sqlalchemy.orm import Session
from dependencies.users import get_current_active_user
from schemas.base import HTTPException, ListResponseBody
from schemas.users import User, UsersQuery

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=ListResponseBody[list[User]])
def read_users(query: UsersQuery = Depends(), db: Session = Depends(get_db)):
    users = get_users(db, skip=query.page_num - 1, limit=query.limit)
    return ListResponseBody(items=users.items, page_num=query.page_num, limit=query.limit, total=users.total)


@router.get("/myself", response_class=User)
async def read_myself(user=Depends(get_current_active_user)):
    return user


@router.get("/{nt_account}", response_model=User)
def read_user(nt_account: str, db: Session = Depends(get_db)):
    db_user = get_user(db, nt_account)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found")

    return db_user


@router.post("/", response_model=User)
def create_user(user: UserBase = Body(), db: Session = Depends(get_db)):
    # db_user = get_user(db, email=user.email)
    # if db_user:
    # raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
