from loguru import logger
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.users import UserModel
from schemas.base import ListResultFromDB
from schemas.users import User, UserBase


async def get_user(db: AsyncIOMotorDatabase, username: str):
    return await db.users.find_one({"username": username, "is_active": True})


def get_users(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> ListResultFromDB[User]:
    # students = await db.users.find().to_list(1000)
    # return students
    # return ListResultFromDB(total=db.query(UserModel).count(), items=db.query(UserModel).order_by(
    #     UserModel.user_id).offset(skip).limit(limit).all())
    pass


def create_user(db: Session, user: UserBase):
    db_user = UserModel(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
