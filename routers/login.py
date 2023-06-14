from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from dao.users import get_user_by_username
from database.mongo import get_db
from schemas.base import APIRouter, HTTPException
from schemas.users import LoginRes
from utils.utils import create_access_token, verify_password

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("/", response_model=LoginRes)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user_dict = await get_user_by_username(db, form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid username or password"
        )

    info_dict = {
        "user_id": user_dict["user_id"],
        "role": user_dict["role"],
    }
    [access_token, expire_in] = create_access_token(info_dict)
    info_dict["access_token"] = access_token
    info_dict["expire_in"] = expire_in

    return info_dict
