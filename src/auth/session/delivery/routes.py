from fastapi import APIRouter, status

from src.auth.session.delivery.authenticate.authenticate_session_router import authenticate_session_router
from src.shared.infra.api.error_response import InternalServerError

session_routes = APIRouter(
    prefix="/sessions",
    tags=["Auth / Session"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)

session_routes.include_router(authenticate_session_router)
