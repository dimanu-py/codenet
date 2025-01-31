from fastapi import APIRouter, status
from src.social.user.application.signup.user_signup import UserSignup

from src.social.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.social.user.infra.router.user_sign_up_request import UserSignupRequest
from src.social.user.infra.router.user_signup_response import UserSignupResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup/{user_id}", status_code=status.HTTP_201_CREATED)
async def signup_user(user_id: str, request: UserSignupRequest) -> UserSignupResponse:
    user_signup = UserSignup(InMemoryUserRepository())

    await user_signup(
        id_=user_id, name=request.name, username=request.username, email=request.email
    )

    return UserSignupResponse()
