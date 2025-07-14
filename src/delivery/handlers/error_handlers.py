from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.error_response import (
    InternalServerError,
    UnprocessableEntityError,
)
from src.shared.infra.logger.fastapi_file_logger import create_api_logger

logger = create_api_logger(name="codenet")


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error(
        message=f"error - {request.url.path}",
        details={
            "error": {
                "message": str(exc),
                "type": "unexpected_error",
            },
            "method": request.method,
            "source": request.url.path,
        },
    )
    return InternalServerError().as_json()


async def domain_error_handler(
    request: Request,
    exc: DomainError,
) -> JSONResponse:
    logger.error(
        message=f"error - {request.url.path}",
        details={
            "error": exc.to_primitives(),
            "method": request.method,
            "source": request.url.path,
        },
    )
    return UnprocessableEntityError(detail=exc.message).as_json()


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.error(
        message=f"error - {request.url.path}",
        details={
            "error": {"message": str(exc), "type": "validation_error"},
            "method": request.method,
            "source": request.url.path,
        },
    )
    return await request_validation_exception_handler(request, exc)
