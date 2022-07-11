from typing import List, Optional

from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    scopes: List[str]


class DataModel(BaseModel):
    id: int


class CreateResponse(BaseModel):
    data: DataModel
    message: str


class ErrorModel(BaseModel):
    detail: str


class DiscordPayload(BaseModel):
    content: str


class PaginationModel(BaseModel):
    count: int = Field(default=None, title="Number of items in this page")
    previous: int = Field(default=None, title="Page number of previous page")
    current: int = Field(default=None, title="Page number of current page")
    next: int = Field(default=None, title="Page number of next page")
    record_count: int = Field(
        default=None, title="Total number of items of the query result"
    )
