import json
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.backoffice.user.infra.api.search.user_search_controller import UserSearchController
from src.shared.delivery.api_parameter import ApiDocExample, QueryParameter
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.success_response import OkResponse

router = APIRouter()

UserFilterQueryParameter = Annotated[
    str,
    QueryParameter(
        description="Filter in JSON format",
        examples=[
            ApiDocExample(name="empty_filter", value="{}"),
            ApiDocExample(name="simple_filter", value='{"field": "username", "equal": "johndoe"}'),
        ],
    ),
]


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
    },
)
@inject
async def get_user_by_criteria(
    filter: UserFilterQueryParameter,
    controller: FromDishka[UserSearchController],
) -> JSONResponse:
    result = await controller.search(filters=json.loads(filter))
    return FastAPIResponse.as_json(result)
