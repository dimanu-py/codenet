from fastapi import Request
from fastapi.responses import JSONResponse

from src.delivery.routers.fastapi_response import FastAPIResponse
from src.shared.infra.http.error_response import (
    InternalServerError,
    UnprocessableEntityError,
)


async def unexpected_exception_handler(
    _: Request,
    __: Exception,
) -> JSONResponse:
    return FastAPIResponse.as_json(InternalServerError())


async def sindri_validation_error_handler(
    _: Request,
    error: Exception,
) -> JSONResponse:
    return FastAPIResponse.as_json(
        UnprocessableEntityError(error={"type": "validation_error", "message": error.message})
    )
