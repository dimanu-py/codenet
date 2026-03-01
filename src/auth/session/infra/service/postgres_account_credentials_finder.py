from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.infra.persistence.account_model import AccountModel
from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.account_by_login_identifier_criteria import AccountByLoginIdentifierCriteria
from src.auth.session.domain.account_credentials_finder import AccountCredentialsFinder
from src.auth.session.domain.login_identifier import LoginIdentifier
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import CriteriaToSqlalchemyConverter


class PostgresAccountCredentialsFinder(AccountCredentialsFinder):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def find_by_login_identifier(self, login: LoginIdentifier) -> AccountAuthCredentials | None:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(
            model=AccountModel,
            criteria=AccountByLoginIdentifierCriteria.for_login_identifier(login.value),
        ).limit(1)
        account = await self._session.scalar(query)

        return AccountAuthCredentials(
            account_id=account.id,
            password=account.password,
            status=account.status,
        ) if account else None
