from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from dao.users import get_user_by_id
from database.mongo import get_db
from handlers import HTTPException
from schemas.users import UserRes
from utils.utils import verifyToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="myself")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_db)):
    user_id = verifyToken(token).get("user_id")
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found")

    return user


async def get_current_active_user(current_user: UserRes = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
