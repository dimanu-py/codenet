from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.delivery.alembic_migrator import AlembicMigrator
from src.social.user.infra.api.search import search_user_router as search_user
from src.social.user.infra.api.signup import signup_user_router as signup_user
from src.shared.infra.http.http_response import HttpResponse


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    migrator = AlembicMigrator()
    await migrator.migrate()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(signup_user.router)
app.include_router(search_user.router)


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return HttpResponse.internal_error(exc)
