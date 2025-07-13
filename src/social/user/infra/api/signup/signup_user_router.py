from collections.abc import AsyncGenerator

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.response import ErrorResponse, SuccessResponse
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

    try:
        await user_signup(command)
    except DomainError as error:
        return ErrorResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.message,
        ).as_json()

    return SuccessResponse(
        status_code=status.HTTP_201_CREATED,
        data={"resource": f"/app/users/signup/{user_id}"},
    ).as_json()
