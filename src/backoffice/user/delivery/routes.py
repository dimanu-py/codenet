from fastapi import APIRouter, status

from src.shared.infra.http.error_response import (
    InternalServerError,
)
from src.backoffice.user.delivery.removal import removal_router
from src.backoffice.user.delivery.search import search_router

user_routes = APIRouter(
    prefix="/users",
    tags=["Social / Users"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

user_routes.include_router(search_router.router)
user_routes.include_router(removal_router.router)
