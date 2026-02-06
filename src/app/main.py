from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from sindripy.value_objects import SindriValidationError

from src.app.alembic_migrator import AlembicMigrator
from src.app.handlers.error_handlers import (
    sindri_validation_error_handler,
    unexpected_exception_handler,
)
from src.app.middleware.fast_api_log_middleware import FastapiLogMiddleware
from src.auth.routes import auth_routes
from src.shared.infra.logger.fastapi_file_logger import (
    create_api_logger,
)
from src.social.routes import social_routes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


logger = create_api_logger(name="codenet")

app = FastAPI(lifespan=lifespan)

app.add_middleware(FastapiLogMiddleware, logger=logger)  # type: ignore
app.add_middleware(CorrelationIdMiddleware)  # type: ignore

app.add_exception_handler(Exception, unexpected_exception_handler)
app.add_exception_handler(SindriValidationError, sindri_validation_error_handler)

app.include_router(social_routes)
app.include_router(auth_routes)
