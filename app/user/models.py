from sqlalchemy import Column, Integer, String, Text, Boolean

from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(40), nullable=False)
    hashed_password = Column(Text, nullable=False)
    email = Column(String(40), nullable=False)
    full_name = Column(Text, nullable=False)
    disabled = Column(Boolean, default=False)

class UserPermission(Base):
    __tablename__ = "user_permission"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    permission = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
