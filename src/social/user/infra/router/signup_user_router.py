from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.http_response import HttpResponse
from src.shared.infra.log.logger import create_logger
from src.shared.infra.persistence.sqlalchemy.base import Base
from src.shared.infra.settings import Settings
from src.shared.infra.http.status_code import StatusCode
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from src.social.user.infra.router.user_sign_up_request import UserSignupRequest

router = APIRouter(prefix="/users", tags=["Users"])
user_logger = create_logger("user")


async def engine_generator() -> AsyncEngine:  # type: ignore
    engine = create_async_engine(Settings().postgres_url)  # type: ignore

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@router.post("/signup/{user_id}", status_code=status.HTTP_201_CREATED)
async def signup_user(
    user_id: str,
    request: UserSignupRequest,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    user_logger.info("User signup request received", extra={"extra": {"id": user_id}})
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
        user_logger.error(
            "User signup failed", extra={"extra": {"error": error.to_dict()}}
        )
        return HttpResponse.domain_error(error, status_code=StatusCode.BAD_REQUEST)

    return HttpResponse.created()
