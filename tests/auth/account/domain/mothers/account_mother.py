from src.auth.account.domain.account import AccountPrimitives
from tests.auth.account.domain.mothers.account_created_at_primitives_mother import AccountCreatedAtPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.domain.mothers.account_status_primitives_mother import AccountStatusPrimitivesMother


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
