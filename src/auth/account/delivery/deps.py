from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.shared.delivery.db_session import get_async_session


def postgres_account_repository(
    session: AsyncSession = Depends(get_async_session),
) -> PostgresAccountRepository:
    return PostgresAccountRepository(session)
