from fastapi import APIRouter, status

from src.auth.account.delivery.signup.signup_router import signup_router
from src.shared.infra.api.error_response import InternalServerError

account_routes = APIRouter(
    prefix="/account",
    tags=["Auth / Account"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

account_routes.include_router(signup_router)
