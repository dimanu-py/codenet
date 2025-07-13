from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.delivery.alembic_migrator import AlembicMigrator
from src.shared.infra.http.response import ErrorResponse
from src.social.user.infra.api import routes as user_routes


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_routes.routes)


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred.",
    ).as_json()
