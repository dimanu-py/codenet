from collections.abc import AsyncGenerator

from fastapi import APIRouter, status, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.infra.http.success_response import CreatedResponse
from src.shared.infra.settings import Settings
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository
from src.social.user.infra.api.signup.user_sign_up_request import UserSignupRequest

router = APIRouter()


async def engine_generator() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(Settings().postgres_url)  # type: ignore

    try:
        yield engine
    finally:
        await engine.dispose()


@router.post(
    "/{user_id}",
    responses={
        status.HTTP_201_CREATED: {"model": CreatedResponse},
    },
)
async def signup_user(
    request: UserSignupRequest,
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    repository: UserRepository = Depends(postgres_user_repository),
) -> JSONResponse:
    command = UserSignupCommand(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
    )

    user_signup = UserSignup(repository)
    await user_signup(command)

    return CreatedResponse(
        data={"resource": f"/app/users/{user_id}"},
    ).as_json()
