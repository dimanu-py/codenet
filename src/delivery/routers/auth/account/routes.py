from fastapi import APIRouter, status

from src.shared.infra.http.error_response import InternalServerError

routes = APIRouter(
    prefix="/account",
    tags=["Auth / Account"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerError,
            "description": "Internal Server Error",
        },
    },
)
