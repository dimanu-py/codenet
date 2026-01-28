from fastapi import APIRouter, status

from src.delivery.routers.user import removal_user_router, search_user_router, signup_user_router as signup_router
from src.shared.infra.http.error_response import (
    InternalServerError,
)

routes = APIRouter(
    prefix="/app/users",
    tags=["Users"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

routes.include_router(signup_router.router)
routes.include_router(search_user_router.router)
routes.include_router(removal_user_router.router)
