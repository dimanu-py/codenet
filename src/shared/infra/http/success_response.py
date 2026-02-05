from abc import ABC
from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel, Field


class SuccessResponse(ABC, BaseModel):
    status: int
    result: Literal["success"] = "success"
    data: dict | list[dict]


class OkResponse(SuccessResponse):
    status: int = Field(default=HTTPStatus.OK)


class AcceptedResponse(SuccessResponse):
    status: int = Field(default=HTTPStatus.ACCEPTED)
    data: dict = Field(default={"accepted": True})
