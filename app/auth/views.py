from datetime import timedelta
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.config import Settings

from fastapi_jwt_auth import AuthJWT

from app.auth.services import REFRESH_TOKEN_EXPIRES_MINUTES, authenticate_user, create_access_token, create_refresh_token
from app.auth.services import ACCESS_TOKEN_EXPIRES_MINUTES

from sqlalchemy.orm import Session

from app.auth.schemas import Token
from app.deps import get_db
from app.user.schemas import User
from app.user.services import UserManager

auth_router = APIRouter()

@auth_router.post("/login", summary="Create access and refresh tokens for user", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user_to_auth = UserManager.get_user_by_username(db, form_data.username)
    user = authenticate_user(user_to_auth, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = Authorize.create_access_token(subject=form_data.username)
    refresh_token = Authorize.create_refresh_token(subject=form_data.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

@auth_router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    #Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

@auth_router.get("/sample")
def sample(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    
    return os.environ
