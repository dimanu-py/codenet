from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from starlette.responses import JSONResponse

from src.shared.infra.http.error_response import ResourceNotFoundError
from src.shared.infra.http.success_response import AcceptedResponse
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


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
    },
)
async def remove_user(
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    command = UserRemovalCommand(user_id=user_id)
    repository = PostgresUserRepository(engine=engine)
    user_remover = UserRemover(repository)

    await user_remover(command)

    return AcceptedResponse(
        data={"message": "User removal request has been accepted."},
    ).as_json()
