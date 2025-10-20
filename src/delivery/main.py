from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from src.delivery.alembic_migrator import AlembicMigrator
from src.delivery.handlers.error_handlers import (
    unexpected_exception_handler,
)
from src.delivery.middleware.fast_api_log_middleware import FastapiLogMiddleware
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

app.add_middleware(FastapiLogMiddleware, logger=logger)  # type: ignore
app.add_middleware(CorrelationIdMiddleware)  # type: ignore
app.add_exception_handler(Exception, unexpected_exception_handler)
app.include_router(user_routes.routes)
