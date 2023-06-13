from motor.motor_asyncio import AsyncIOMotorDatabase
from models.users import UserModel
from schemas.base import ListResultFromDB
from schemas.users import UserRes, UserToCreate


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str):
    return await db.users.find_one({"username": username, "is_active": True})


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: int):
    return await db.users.find_one({"user_id": user_id, "is_active": True})


async def get_users(db: AsyncIOMotorDatabase, skip: int, limit: int, condition_dict: dict) -> ListResultFromDB[UserRes]:
    users = await db.users.find(condition_dict, {"_id": 0, "password": 0, "is_active": 0}).skip(skip).limit(limit).to_list(limit)
    total = await db.users.count_documents(condition_dict)

    return ListResultFromDB(
        items=users,
        total=total
    )


async def add_user(db: AsyncIOMotorDatabase, user: UserToCreate):
    user_id = 0
    docs = await db.users.find().sort([('age', -1)]).limit(1).to_list(1)
    if docs:
        user_id = docs[0]["user_id"] + 1
    db_user = UserModel(
        user_id=user_id,
        **user.dict()
    ).dict()

    await db.users.insert_one(db_user)
    return db_user
