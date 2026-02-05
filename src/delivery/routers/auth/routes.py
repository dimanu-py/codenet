from fastapi import APIRouter, status

from src.delivery.routers.auth.account.routes import routes as account_routes
from src.shared.infra.http.error_response import InternalServerError

routes = APIRouter(
    prefix="/app/auth",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

routes.include_router(account_routes)