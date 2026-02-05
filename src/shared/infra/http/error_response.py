from abc import ABC
from http import HTTPStatus
from typing import Literal

from pydantic import Field, BaseModel


class ErrorResponse(ABC, BaseModel):
    status: int
    result: Literal["error"] = "error"
    error: dict


class UnprocessableEntityError(ErrorResponse):
    status: int = Field(default=HTTPStatus.UNPROCESSABLE_ENTITY)
    error: dict = Field(default={"message": HTTPStatus.UNPROCESSABLE_ENTITY.phrase})


class ResourceNotFoundError(ErrorResponse):
    status: int = Field(default=HTTPStatus.NOT_FOUND)
    error: dict = Field(default={"message": HTTPStatus.NOT_FOUND.phrase})


class ConflictErrorResponse(ErrorResponse):
    status: int = Field(default=HTTPStatus.CONFLICT)
    error: dict = Field(default={"message": HTTPStatus.CONFLICT.phrase})


class InternalServerError(ErrorResponse):
    status: int = Field(default=HTTPStatus.INTERNAL_SERVER_ERROR)
    error: dict = Field(default={"message": HTTPStatus.INTERNAL_SERVER_ERROR.phrase})
