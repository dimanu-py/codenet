from fastapi import APIRouter, status

from src.shared.infra.http.response import ErrorResponse
from src.social.user.infra.api.removal import removal_user_router as removal_router
from src.social.user.infra.api.search import search_user_router as search_router
from src.social.user.infra.api.signup import signup_user_router as signup_router

routes = APIRouter(
    prefix="/app/users",
    tags=["Users"],
    responses={
	    status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Bad Request"},
	    status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Unauthorized"},
	    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse, "description": "Unprocessable Entity"},
	    status.HTTP_429_TOO_MANY_REQUESTS: {"model": ErrorResponse, "description": "Too Many Requests"},
	    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)

routes.include_router(signup_router.router)
routes.include_router(search_router.router)
routes.include_router(removal_router.router)
