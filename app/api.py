from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models import ErrorModel

api_router = APIRouter(default_response_class=ORJSONResponse)
from app.auth.views import auth_router
from app.user.views import user_router

api_router.include_router(
    auth_router,
    prefix="",
    tags=["root"],
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)

api_router.include_router(
    user_router,
    prefix="/user",
    tags=["users"],
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)