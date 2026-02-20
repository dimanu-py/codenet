from fastapi import APIRouter, status

from src.auth.account.delivery.authenticate.authenticate_account_router import authenticate_account_router
from src.auth.account.delivery.signup.signup_account_router import signup_account_router
from src.shared.infra.api.error_response import InternalServerError

account_routes = APIRouter(
    prefix="/accounts",
    tags=["Auth / Account"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

account_routes.include_router(authenticate_account_router)
account_routes.include_router(signup_account_router)
