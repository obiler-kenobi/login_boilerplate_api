from app.auth.services import get_password_hash
from app.user.schemas import UserCreate, UserPermissionBase

from app.user import models
from app.user.schemas import UserCreate

from sqlalchemy.orm import Session

class UserManager(object):
    @staticmethod
    def get_all_users(db: Session):
        return db.query(models.User).all()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        new_user = models.User(**user.dict())

        new_user.hashed_password = get_password_hash(new_user.hashed_password)

        db.add(new_user)
        db.commit()
        return new_user

class UserPermissionManager(object):
    @staticmethod
    def get_all_permissions(db: Session):
        return db.query(models.UserPermission).all()

    @staticmethod
    def create_user_permission(db: Session, user_permission: UserPermissionBase):
        new_user_permission = models.UserPermission(**user_permission.dict())

        db.add(new_user_permission)
        db.commit()
        return new_user_permission

    @staticmethod
    def get_permission_scopes(db: Session):
        permissions = db.query(models.UserPermission).all()

        scopes = {}

        for permission in permissions:
            scopes[permission.permission] = permission.description

        return scopes


    



