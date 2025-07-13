import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.delivery.alembic_migrator import AlembicMigrator
from src.delivery.middleware.fast_api_log_middleware import FastapiLogMiddleware
from src.shared.infra.http.response import ErrorResponse
from src.shared.infra.logger.fastapi_file_logger import FastApiFileLogger
from src.shared.infra.logger.file_rotating_handler import TimeRotatingFileHandler
from src.social.user.infra.api import routes as user_routes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


logger = FastApiFileLogger(
    name="ipy_monitoring",
    handlers=[
        TimeRotatingFileHandler.create(
            file_name="production",
            level_to_record=logging.ERROR,
        ),
        TimeRotatingFileHandler.create(
            file_name="dev",
            level_to_record=logging.DEBUG,
        ),
    ],
)

app = FastAPI(lifespan=lifespan)

app.add_middleware(FastapiLogMiddleware, logger=logger)
app.include_router(user_routes.routes)


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred.",
    ).as_json()
