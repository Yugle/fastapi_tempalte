from fastapi import APIRouter, Depends, Body, status
from dao.users import *
from database.mongo import get_db
from dependencies.users import get_current_active_user
from schemas.base import HTTPException, ListResponseBody
from schemas.users import UserRes, UsersQuery, UserToCreate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=ListResponseBody[list[UserRes]])
async def read_users(query: UsersQuery = Depends(), db: AsyncIOMotorDatabase = Depends(get_db)):
    users = await get_users(db, skip=(query.page_num - 1) * 10, limit=query.limit, condition_dict=query.parse_condition_dict())

    return ListResponseBody(items=users.items, page_num=query.page_num, limit=query.limit, total=users.total)


@router.get("/myself", response_model=UserRes)
async def read_myself(user=Depends(get_current_active_user)):
    return user


@router.get("/{user_id}", response_model=UserRes)
async def read_user(user_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    db_user = await get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found")

    return db_user


@router.post("/", response_model=UserRes)
async def create_user(user: UserToCreate = Body(), db: AsyncIOMotorDatabase = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, message="This user is already registered")
    return await add_user(db=db, user=user)
