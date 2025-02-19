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
from src.social.user.application.search.user_searcher import UserSearcher
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


@router.get("/search/")
async def get_user_by_criteria(
    filters: str,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    query = SearchUserQuery(filters=json.loads(filters))
    repository = PostgresUserRepository(engine=engine)
    user_searcher = UserSearcher(repository=repository)

    try:
        user = await user_searcher(query)
    except DomainError as error:
        return HttpResponse.domain_error(error, status_code=StatusCode.BAD_REQUEST)

    return HttpResponse.ok(user.to_dict() if user else {})
