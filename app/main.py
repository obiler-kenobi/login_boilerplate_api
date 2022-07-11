from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router

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