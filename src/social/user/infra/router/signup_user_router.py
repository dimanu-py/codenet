from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.shared.infra.HttpResponse import HttpResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.social.user.infra.router.user_sign_up_request import UserSignupRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup/{user_id}", status_code=status.HTTP_201_CREATED)
async def signup_user(user_id: str, request: UserSignupRequest) -> JSONResponse:
    command = UserSignupCommand(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
    )
    user_signup = UserSignup(InMemoryUserRepository())

    await user_signup(command)

    return HttpResponse.created()
