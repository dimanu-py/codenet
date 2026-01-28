import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.delivery.routers.user.deps import postgres_user_repository
from src.shared.infra.http.success_response import OkResponse
from src.social.user.application.search.user_searcher import UserSearcher
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.search.user_search_controller import UserSearchController

router = APIRouter()


def get_use_case(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSearcher:
    return UserSearcher(repository=repository)


def get_controller(
    use_case: UserSearcher = Depends(get_use_case),
) -> UserSearchController:
    return UserSearchController(use_case=use_case)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
    },
)
async def get_user_by_criteria(
    filter: str = Query(openapi_examples={"simple_filter": Example(value='{"field": "username", "equal": "johndoe"}')}),
    controller: UserSearchController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.search(filters=json.loads(filter))
    return result.as_json()
