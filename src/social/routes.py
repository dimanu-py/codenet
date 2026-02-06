from fastapi import APIRouter, status

from src.shared.infra.http.error_response import InternalServerError
from src.social.user.delivery.routes import user_routes

social_routes = APIRouter(
    prefix="/app/social",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

social_routes.include_router(user_routes)
