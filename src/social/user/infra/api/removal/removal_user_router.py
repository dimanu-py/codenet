from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.http_response import HttpResponse
from src.shared.infra.http.status_code import StatusCode
from src.shared.infra.settings import Settings
from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.application.removal.user_remover import UserRemover
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


@router.delete("/removal/{user_id}")
async def remove_user(
    user_id: str,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    command = UserRemovalCommand(user_id=user_id)
    repository = PostgresUserRepository(engine=engine)
    user_remover = UserRemover(repository)

    try:
        await user_remover(command)
    except DomainError as error:
        return HttpResponse.domain_error(error, status_code=StatusCode.BAD_REQUEST)

    return HttpResponse.ok(content={})
