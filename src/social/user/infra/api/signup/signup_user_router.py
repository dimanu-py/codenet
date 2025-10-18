from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from src.shared.infra.http.success_response import CreatedResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository
from src.social.user.infra.api.signup.user_sign_up_request import UserSignupRequest

router = APIRouter()


def user_signup_use_case(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSignup:
    return UserSignup(repository)


@router.post(
    "/{user_id}",
    responses={
        status.HTTP_201_CREATED: {"model": CreatedResponse},
    },
)
async def signup_user(
    request: UserSignupRequest,
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    user_signup: UserSignup = Depends(user_signup_use_case),
) -> JSONResponse:
    command = UserSignupCommand(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
    )

    await user_signup.execute(command)

    return CreatedResponse(
        data={"resource": f"/app/users/{user_id}"},
    ).as_json()
