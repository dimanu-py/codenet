from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.delivery.alembic_migrator import AlembicMigrator
from src.delivery.handlers.error_handlers import (
    application_error_handler,
    domain_error_handler,
    unexpected_exception_handler,
    validation_error_handler,
)
from src.delivery.middleware.fast_api_log_middleware import FastapiLogMiddleware
from src.shared.domain.exceptions.application_error import ApplicationError
from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.logger.fastapi_file_logger import (
    create_api_logger,
)
from src.social.user.infra.api import routes as user_routes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


logger = create_api_logger(name="codenet")

app = FastAPI(lifespan=lifespan)

app.add_middleware(FastapiLogMiddleware, logger=logger)
app.add_exception_handler(Exception, unexpected_exception_handler)
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(ApplicationError, application_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.include_router(user_routes.routes)
