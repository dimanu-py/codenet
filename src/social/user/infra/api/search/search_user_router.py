import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.shared.infra.http.success_response import OkResponse
from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_search_response import UserSearchResponse
from src.social.user.application.search.user_searcher import UserSearcher
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository

router = APIRouter()


def user_searcher_use_case(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSearcher:
    return UserSearcher(repository=repository)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
    },
)
async def get_user_by_criteria(
    filter: str = Query(examples=['{"field": "username", "equal": "john_doe"}']),
    user_searcher: UserSearcher = Depends(user_searcher_use_case),
) -> JSONResponse:
    query = SearchUserQuery(filters=json.loads(filter))

    users = await user_searcher(query)
    response = UserSearchResponse([user.to_primitives() for user in users])

    return OkResponse(
        data=response.dump(),
    ).as_json()
