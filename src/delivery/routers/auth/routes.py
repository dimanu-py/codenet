from fastapi import APIRouter, status

from src.delivery.routers.auth.account.routes import account_routes
from src.shared.infra.http.error_response import InternalServerError

auth_routes = APIRouter(
    prefix="/app/auth",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

auth_routes.include_router(account_routes)