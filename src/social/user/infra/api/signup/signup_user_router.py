from collections.abc import AsyncGenerator

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.infra.http.success_response import SuccessResponse
from src.shared.infra.settings import Settings
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.infra.api.signup.user_sign_up_request import UserSignupRequest
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)

router = APIRouter()


async def engine_generator() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(Settings().postgres_url)  # type: ignore

    try:
        yield engine
    finally:
        await engine.dispose()


@router.post(
    "/signup/{user_id}",
    responses={
        status.HTTP_201_CREATED: {"model": SuccessResponse},
    },
)
async def signup_user(
    user_id: str,
    request: UserSignupRequest,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    command = UserSignupCommand(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
    )
    repository = PostgresUserRepository(engine=engine)
    user_signup = UserSignup(repository)

    await user_signup(command)

    return SuccessResponse(
        status_code=status.HTTP_201_CREATED,
        data={"resource": f"/app/users/signup/{user_id}"},
    ).as_json()
