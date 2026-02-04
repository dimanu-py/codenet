from fastapi import Request
from fastapi.responses import JSONResponse
from sindripy.value_objects import SindriValidationError

from src.shared.infra.http.error_response import (
    InternalServerError, UnprocessableEntityError,
)


async def unexpected_exception_handler(
    _: Request,
    __: Exception,
) -> JSONResponse:
    return InternalServerError().as_json()


async def sindri_validation_error_handler(
    _: Request,
    error: SindriValidationError,
) -> JSONResponse:
    return UnprocessableEntityError(detail={"message": error.message}).as_json()
