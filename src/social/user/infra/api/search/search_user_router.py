import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.http_response import HttpResponse
from src.shared.infra.http.status_code import StatusCode
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


@router.get("/search/")
async def get_user_by_criteria(
    filter: str,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    query = SearchUserQuery(filters=json.loads(filter))
    repository = PostgresUserRepository(engine=engine)
    user_searcher = UserSearcher(repository=repository)

    try:
        users = await user_searcher(query)
        response = UserSearchResponse([user.to_primitives() for user in users])
    except DomainError as error:
        return HttpResponse.domain_error(error, status_code=StatusCode.BAD_REQUEST)

    return HttpResponse.ok(response.dump())
