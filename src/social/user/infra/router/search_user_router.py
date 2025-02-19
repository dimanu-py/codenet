from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.shared.infra.settings import Settings

router = APIRouter(prefix="/users", tags=["Users"])


async def engine_generator() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(Settings().postgres_url)  # type: ignore

    try:
        yield engine
    finally:
        await engine.dispose()


@router.get("/search/")
async def get_user_by_criteria(
    filters: str,
    engine: AsyncEngine = Depends(engine_generator),
) -> JSONResponse:
    raise NotImplementedError
