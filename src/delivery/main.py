import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.delivery.alembic_migrator import AlembicMigrator
from src.delivery.middleware.fast_api_log_middleware import FastapiLogMiddleware
from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.response import ErrorResponse
from src.shared.infra.logger.fastapi_file_logger import FastApiFileLogger
from src.shared.infra.logger.file_rotating_handler import TimeRotatingFileHandler
from src.social.user.infra.api import routes as user_routes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


logger = create_api_logger(name="codenet")

app = FastAPI(lifespan=lifespan)

app.add_middleware(FastapiLogMiddleware, logger=logger)
app.include_router(user_routes.routes)


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        message=f"error - {request.url.path}",
        details={
            "error": {"message": str(exc), "type": "unexpected_error"},
            "method": request.method,
            "source": request.url.path,
        },
    )
    return ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred.",
    ).as_json()


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    logger.error(
        message=f"error - {request.url.path}",
        details={
            "error": exc.to_primitives(),
            "method": request.method,
            "source": request.url.path,
        },
    )
    return ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=exc.message,
    ).as_json()


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
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
