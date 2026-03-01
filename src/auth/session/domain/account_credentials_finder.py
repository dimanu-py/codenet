from abc import ABC, abstractmethod

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.login_identifier import LoginIdentifier


class AccountCredentialsFinder(ABC):
    @abstractmethod
    async def find_by_login_identifier(self, login: LoginIdentifier) -> AccountAuthCredentials | None:
        raise NotImplementedError
