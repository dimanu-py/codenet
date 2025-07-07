from fastapi import APIRouter

from src.social.user.infra.api.removal import removal_user_router as removal_router
from src.social.user.infra.api.search import search_user_router as search_router
from src.social.user.infra.api.signup import signup_user_router as signup_router

routes = APIRouter(prefix="/app/users", tags=["Users"])

routes.include_router(signup_router.router)
routes.include_router(search_router.router)
routes.include_router(removal_router.router)
