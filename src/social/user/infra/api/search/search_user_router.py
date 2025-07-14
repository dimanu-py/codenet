import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.infra.http.response import SuccessResponse
from src.shared.infra.settings import Settings
from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_search_response import UserSearchResponse
from src.social.user.application.search.user_searcher import UserSearcher
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


@router.get(
    "/search",
    responses={
        status.HTTP_200_OK: {"model": SuccessResponse},
    },
)
async def get_user_by_criteria(
    filter: str,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    query = SearchUserQuery(filters=json.loads(filter))
    repository = PostgresUserRepository(engine=engine)
    user_searcher = UserSearcher(repository=repository)

    users = await user_searcher(query)
    response = UserSearchResponse([user.to_primitives() for user in users])

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=response.dump(),
    ).as_json()
