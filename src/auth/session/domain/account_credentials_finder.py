from abc import ABC, abstractmethod

from src.auth.session.domain.credentials import Credentials
from src.auth.session.domain.login import Login


class AccountCredentialsFinder(ABC):
    @abstractmethod
    def find_by_login_information(self, login: Login) -> Credentials:
        raise NotImplementedError
