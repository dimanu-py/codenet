from abc import ABC, abstractmethod

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.login_identifier import LoginIdentifier
from src.shared.domain.value_objects.optional import Optional


class AccountCredentialsFinder(ABC):
    @abstractmethod
    async def find_by_login_identifier(self, login: LoginIdentifier) -> Optional[AccountAuthCredentials]:
        raise NotImplementedError
