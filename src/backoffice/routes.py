from fastapi import APIRouter, status

from src.backoffice.user.delivery.routes import user_routes
from src.shared.infra.api.error_response import InternalServerError

social_routes = APIRouter(
    prefix="/app/backoffice",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

social_routes.include_router(user_routes)
