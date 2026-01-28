from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.infra.settings import Settings
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)

settings = Settings()  # type: ignore
engine = create_async_engine(str(settings.postgres_url))


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def postgres_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> PostgresUserRepository:
    return PostgresUserRepository(session)
