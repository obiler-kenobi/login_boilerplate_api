from fastapi import Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from fastapi_jwt_auth import AuthJWT

from app.auth.services import (SECRET_KEY, ALGORITHM, get_user_authenticated, fake_users_db)
from app.auth.schemas import TokenData
from app.user.schemas import User

from app.database import SessionLocal
from app.user.services import UserManager, UserPermissionManager
from sqlalchemy.orm import Session

# FastAPI Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
    #Scopes [Authorization]
    )

async def get_current_user(
    security_scopes: SecurityScopes,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)):
    Authorize.jwt_required()

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        username: str = Authorize.get_jwt_subject()
        if username is None:
            raise credentials_exception
        token_scopes = ["me","create_user","sample"]
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = UserManager.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return user

async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["sample"])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

def get_scopes(db: Session = Depends(get_db)):
    return UserPermissionManager.get_permission_scopes(db)

