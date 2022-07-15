from datetime import timedelta
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.services import REFRESH_TOKEN_EXPIRES_MINUTES, authenticate_user, create_access_token, create_refresh_token
from app.auth.services import ACCESS_TOKEN_EXPIRES_MINUTES

from sqlalchemy.orm import Session

from app.auth.schemas import Token
from app.deps import get_db
from app.user.schemas import User
from app.user.services import UserManager

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_to_auth = UserManager.get_user_by_username(db, form_data.username)
    user = authenticate_user(user_to_auth, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@auth_router.get("/sample")
def sample():
    return os.environ
