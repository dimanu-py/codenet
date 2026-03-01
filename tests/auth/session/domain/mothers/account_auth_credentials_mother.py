from sindripy.mothers import ObjectMother

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials


class AccountAuthCredentialsMother(ObjectMother):
    @classmethod
    def with_password(cls, password: str) -> AccountAuthCredentials:
        return AccountAuthCredentials(
            account_id=cls._faker().uuid4(),
            password=password,
            status=cls._faker().word(),
        )
