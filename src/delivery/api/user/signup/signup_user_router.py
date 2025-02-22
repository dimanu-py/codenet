from collections.abc import AsyncGenerator

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.delivery.api.user.signup.user_sign_up_request import UserSignupRequest
from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.http_response import HttpResponse
from src.shared.infra.http.status_code import StatusCode
from src.shared.infra.settings import Settings
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)

router = APIRouter(prefix="/users", tags=["Users"])


async def engine_generator() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(Settings().postgres_url)  # type: ignore

    try:
        yield engine
    finally:
        await engine.dispose()


@router.post("/signup/{user_id}", status_code=status.HTTP_201_CREATED)
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
        return HttpResponse.domain_error(error, status_code=StatusCode.BAD_REQUEST)

    return HttpResponse.created(resource=f"/users/signup/{user_id}")
