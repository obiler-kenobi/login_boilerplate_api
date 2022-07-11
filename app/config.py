import os
import re
from enum import Enum
from typing import Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings
from pydantic.networks import HttpUrl

load_dotenv()


class ENVEnum(str, Enum):
    production: str = "production"
    prod: str = "prod"
    uat: str = "uat"
    staging: str = "staging"
    development: str = "development"
    dev: str = "dev"
    testing: str = "testing"
    local: str = "local"

#
# class DatabaseConfig(BaseModel):
#     database: str = os.environ["POSTGRES_DB"]
#     user: str = os.environ["POSTGRES_USER"]
#     password: str = os.environ["POSTGRES_PASSWORD"]
#     host: str = os.environ["POSTGRES_HOST"]
#     port: int = int(os.environ["POSTGRES_PORT"])
#     autorollback: bool = True
#     sslmode: str = "disable"
#     max_connections: int = int(os.environ["DB_MAX_CONNECTIONS"])


class APIConfig(BaseModel):
    url: HttpUrl
    timeout: Optional[int]
    jwt: Optional[str]
    token: Optional[str]


class Settings(BaseSettings):
    ENV: ENVEnum = ENVEnum(os.environ["ENV"])
    APP_NAME: str = os.environ["APP_NAME"]
    VERSION: str = os.environ["VERSION"]
    # DATABASE: DatabaseConfig = DatabaseConfig()
    DB_MAX_RETRY: int = int(os.environ["DB_MAX_RETRY"])
    DB_RECONNECT_DELAY: int = int(os.environ["DB_RECONNECT_DELAY"])
    SERVICE_TYPE: str = os.environ["SERVICE_TYPE"]
    IS_CONSUMER: bool = SERVICE_TYPE == "consumer"
    TIMEZONE: str = os.environ["TZ"]
    API_MAX_RETRY: int = int(os.environ["API_MAX_RETRY"])
    API_BACKOFF_FACTOR: int = int(os.environ["API_BACKOFF_FACTOR"])
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S%z"
    LOG_LEVEL: str = os.environ["LOG_LEVEL"]
    ROLE_NAME: str = re.sub(r"-api$", "", APP_NAME)
    ALLOWED_ROLE_NAMES: List = [APP_NAME, ROLE_NAME, f"{ROLE_NAME}-web"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    ALGORITHM: str = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

settings = Settings()