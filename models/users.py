from sqlalchemy import Boolean, Column, Integer, String
from database.sql_server import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    nt_account = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    role = Column(Integer, index=True)
    is_active = Column(Boolean, default=True)
