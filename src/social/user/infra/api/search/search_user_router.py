import json

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse

from src.shared.infra.http.success_response import OkResponse
from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_search_response import UserSearchResponse
from src.social.user.application.search.user_searcher import UserSearcher
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
    },
)
async def get_user_by_criteria(
    filter: str = Query(examples=['{"field": "username", "equal": "john_doe"}']),
    repository: UserRepository = Depends(postgres_user_repository),
) -> JSONResponse:
    query = SearchUserQuery(filters=json.loads(filter))

    user_searcher = UserSearcher(repository=repository)
    users = await user_searcher(query)
    response = UserSearchResponse([user.to_primitives() for user in users])

    return OkResponse(
        data=response.dump(),
    ).as_json()
