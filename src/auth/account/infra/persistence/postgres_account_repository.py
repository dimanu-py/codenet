from typing import override

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.application.signup.account_with_user_signup import EmailAlreadyExists
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
        try:
            await self._session.flush()
        except IntegrityError as error:
            if self._is_email_unique_constraint_violation(error):
                raise EmailAlreadyExists() from error
            raise error

    async def search_by_email(self, email: AccountEmail) -> Optional[Account]:
        result = await self._session.execute(select(AccountModel).where(AccountModel.email == email.value))
        account = result.scalar_one_or_none()
        return Optional.lift(account, lambda model: model.to_domain())

    @staticmethod
    def _is_email_unique_constraint_violation(error: IntegrityError) -> bool:
        error_message = str(error.orig)
        return "accounts_email_key" in error_message
