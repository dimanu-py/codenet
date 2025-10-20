from fastapi import Request
from fastapi.responses import JSONResponse

from src.shared.infra.http.error_response import (
    InternalServerError,
)


async def unexpected_exception_handler(
    _: Request,
    __: Exception,
) -> JSONResponse:
    return InternalServerError().as_json()
