from typing import List
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from app.user.schemas import User, UserAuthenticate, UserCreate, UserPermission, UserPermissionBase
from app.deps import get_current_active_user, get_current_user, get_db, get_scopes
from app.user.services import UserManager, UserPermissionManager


user_router = APIRouter()

@user_router.get("/me/", response_model=User)
async def user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = UserManager.get_user_by_username(db, Authorize.get_jwt_subject())
    return current_user
#async def read_users_me(current_user: User = Depends(get_current_active_user)):
#    return current_user

@user_router.get("/me/items/")
async def read_own_items(current_user: User = Security(get_current_active_user, scopes=["items"])):
    return [{"item_id": "Foo", "owner": current_user.username}]

@user_router.get(
    "",
    response_model=List[UserAuthenticate],
    status_code=status.HTTP_200_OK
)
def get_all_users(db: Session = Depends(get_db)):
    return UserManager.get_all_users(db)

@user_router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserManager.create_user(db, user)

#USER PERMISSION
@user_router.get(
    "/user-permissions",
    response_model=List[UserPermission],
    status_code=status.HTTP_200_OK
)
def get_all_user_persmissions(db: Session = Depends(get_db)):
    return UserPermissionManager.get_all_permissions(db)

@user_router.post(
    "/user-permissions",
    response_model=UserPermission,
    status_code=status.HTTP_201_CREATED
)
def create_user_permission(user_permission: UserPermissionBase, db: Session = Depends(get_db)):
    return UserPermissionManager.create_user_permission(db, user_permission)

@user_router.get(
    "/user-permissions/scopes",
    status_code=status.HTTP_200_OK
)
def get_permission_scopes(db: Session = Depends(get_db)):
    return None

