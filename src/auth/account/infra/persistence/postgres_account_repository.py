from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.infra.persistence.account_model import AccountModel
from src.shared.domain.value_objects.optional import Optional


class PostgresAccountRepository(AccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def save(self, account: Account) -> None:
        account_to_save = AccountModel.from_domain(account)
        await self._session.merge(account_to_save)
        await self._session.flush()

    async def search_by_email(self, email: AccountEmail) -> Optional[Account]:
        result = await self._session.execute(
            select(AccountModel).where(AccountModel.email == email.value)
        )
        account = result.scalar_one_or_none()
        return Optional.lift(account, lambda model: model.to_domain())
