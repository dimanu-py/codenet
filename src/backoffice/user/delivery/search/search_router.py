import json

from fastapi import APIRouter, Depends, Query, status
from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.backoffice.user.application.search.user_searcher import UserSearcher
from src.backoffice.user.delivery.deps import postgres_user_repository
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.infra.api.search.user_search_controller import UserSearchController
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.success_response import OkResponse

router = APIRouter()


def get_controller(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSearchController:
    return UserSearchController(use_case=UserSearcher(repository=repository))


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
    },
)
async def get_user_by_criteria(
    filter: str = Query(
        openapi_examples={
            "empty_filter": Example(value="{}"),
            "simple_filter": Example(value='{"field": "username", "equal": "johndoe"}'),
        }
    ),
    controller: UserSearchController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.search(filters=json.loads(filter))
    return FastAPIResponse.as_json(result)
