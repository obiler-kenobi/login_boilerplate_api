from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from fastapi_jwt_auth.exceptions import AuthJWTException
from app.auth.config import Settings
from fastapi_jwt_auth import AuthJWT
from app.database import engine

#MODELS
from app.user import models as user_models

app = FastAPI()

#CREATE TABLE
user_models.Base.metadata.create_all(bind=engine)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@AuthJWT.load_config
def get_config():
    return Settings()