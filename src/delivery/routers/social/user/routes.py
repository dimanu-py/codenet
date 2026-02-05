from fastapi import APIRouter, status

from src.delivery.routers.social.user.removal import removal_router
from src.delivery.routers.social.user.search import search_router
from src.delivery.routers.social.user.signup import signup_router
from src.shared.infra.http.error_response import (
    InternalServerError,
)

routes = APIRouter(
    prefix="/users",
    tags=["Social / Users"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

routes.include_router(signup_router.router)
routes.include_router(search_router.router)
routes.include_router(removal_router.router)
