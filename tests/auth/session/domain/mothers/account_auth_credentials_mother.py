from object_mother import ObjectMother

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials


class AccountAuthCredentialsMother(ObjectMother):
    @classmethod
    def verifiable_with(cls, plain_password: str) -> AccountAuthCredentials:
        return AccountAuthCredentials(
            account_id=cls._faker().uuid4(),
            password=plain_password,
        )
