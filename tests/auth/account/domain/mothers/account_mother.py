from object_mother import ObjectMother

from src.auth.account.domain.account import Account, AccountPrimitives
from tests.auth.account.domain.mothers.account_created_at_primitives_mother import AccountCreatedAtPrimitivesMother
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.domain.mothers.account_status_primitives_mother import AccountStatusPrimitivesMother
from tests.auth.account.domain.mothers.account_username_primitives_mother import AccountUsernamePrimitivesMother


class AccountMother(ObjectMother):
    @staticmethod
    def any() -> Account:
        return Account(
            id=AccountIdPrimitivesMother.any(),
            username=AccountUsernamePrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=AccountPasswordHashPrimitivesMother.any(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.any(),
        )

    @staticmethod
    def dummy() -> Account:
        return Account(
            id=AccountIdPrimitivesMother.dummy(),
            username=AccountUsernamePrimitivesMother.dummy(),
            email=AccountEmailPrimitivesMother.dummy(),
            password=AccountPasswordHashPrimitivesMother.dummy(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.dummy(),
        )

    @classmethod
    def create(cls, **overrides) -> Account:
        default = cls.any().to_primitives()
        return Account(**{**default, **overrides})


class AccountPrimitivesMother:
    @staticmethod
    def dummy() -> AccountPrimitives:
        return AccountPrimitives(
            id=AccountIdPrimitivesMother.any(),
            username="dummy.username",
            email="dummy.email@email.com",
            password=AccountPasswordHashPrimitivesMother.dummy(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.dummy(),
        )

    @staticmethod
    def sharing_email_with(account_primitives: AccountPrimitives) -> AccountPrimitives:
        return AccountPrimitives(
            id=AccountIdPrimitivesMother.any(),
            username="sharing.email",
            email=account_primitives["email"],
            password=AccountPasswordHashPrimitivesMother.dummy(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.dummy(),
        )

    @staticmethod
    def sharing_username_with(account_primitives: AccountPrimitives) -> AccountPrimitives:
        return AccountPrimitives(
            id=AccountIdPrimitivesMother.any(),
            username=account_primitives["username"],
            email="sharing.username.email@email.com",
            password=AccountPasswordHashPrimitivesMother.dummy(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.dummy(),
        )
