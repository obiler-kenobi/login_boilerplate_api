from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
   
    class Config:
        orm_mode = True

class UserAuthenticate(User):
    hashed_password: str


class UserPermissionBase(BaseModel):
    permission: str
    description: str

class UserPermission(UserPermissionBase):
    id: int

    class Config:
        orm_mode = True