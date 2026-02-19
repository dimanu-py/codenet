from typing import override

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email_already_exists import AccountEmailAlreadyExists
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.accounts import Accounts
from src.auth.account.infra.persistence.account_model import AccountModel
from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import CriteriaToSqlalchemyConverter


class PostgresAccountRepository(AccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def save(self, account: Account) -> None:
        account_to_save = AccountModel.from_domain(account)
        self._session.add(account_to_save)
        try:
            await self._session.flush()
        except IntegrityError as error:
            if self._is_email_unique_constraint_violation(error):
                raise AccountEmailAlreadyExists() from error
            raise error

    @override
    async def matching(self, criteria: Criteria) -> Accounts:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(AccountModel, criteria)
        accounts = await self._session.scalars(query)
        return Accounts([account.to_domain() for account in accounts])

    @staticmethod
    def _is_email_unique_constraint_violation(error: IntegrityError) -> bool:
        error_message = str(error.orig)
        return "accounts_email_key" in error_message
