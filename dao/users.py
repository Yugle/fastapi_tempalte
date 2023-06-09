from sqlalchemy.orm import Session
from models.users import UserModel
from schemas.base import ListResultFromDB
from schemas.users import User, UserBase


def get_user(db: Session, nt_account: str):
    return db.query(UserModel).filter(UserModel.nt_account == nt_account).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> ListResultFromDB[User]:
    return ListResultFromDB(total=db.query(UserModel).count(), items=db.query(UserModel).order_by(
        UserModel.user_id).offset(skip).limit(limit).all())


def create_user(db: Session, user: UserBase):
    db_user = UserModel(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
