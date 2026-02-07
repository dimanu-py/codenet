from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.delivery.db_session import get_async_session
from src.backoffice.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)


def postgres_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> PostgresUserRepository:
    return PostgresUserRepository(session)
