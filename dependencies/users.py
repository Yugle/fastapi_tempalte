from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from requests import Session
from dao.users import get_user
from database.sql_server import get_db
from handlers import HTTPException
from schemas.users import User
from utils.utils import verifyToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="myself")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    nt_account = verifyToken(token).get("sub")
    user = get_user(db, nt_account=nt_account)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found")

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
