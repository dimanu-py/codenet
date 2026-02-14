from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sindripy.value_objects import SindriValidationError

from src.app.alembic_migrator import AlembicMigrator
from src.app.handlers.error_handlers import (
    sindri_validation_error_handler,
    unexpected_exception_handler,
)
from src.app.middleware.fast_api_log_middleware import FastapiLogMiddleware
from src.auth.routes import auth_routes
from src.backoffice.routes import social_routes
from src.shared.infra.injector.databse_session_provider import DatabaseSessionProvider
from src.shared.infra.injector.registry import get_registered_providers, register_providers
from src.shared.infra.logger.fastapi_file_logger import (
    create_api_logger,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    basic_app = FastAPI(lifespan=lifespan)
    basic_app.include_router(social_routes)
    basic_app.include_router(auth_routes)
    basic_app.add_exception_handler(Exception, unexpected_exception_handler)
    basic_app.add_exception_handler(SindriValidationError, sindri_validation_error_handler)
    return basic_app


def create_production_app() -> FastAPI:
    production_app = create_app()

    register_providers()
    di_container = make_async_container(*get_registered_providers(), DatabaseSessionProvider())
    setup_dishka(di_container, production_app)

    logger = create_api_logger(name="codenet")
    production_app.add_middleware(FastapiLogMiddleware, logger=logger)  # type: ignore
    production_app.add_middleware(CorrelationIdMiddleware)  # type: ignore

    return production_app


app = create_production_app()
