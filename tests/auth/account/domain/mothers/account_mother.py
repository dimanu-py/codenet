from sindripy.mothers import ObjectMother

from src.auth.account.domain.account import Account
from tests.auth.account.domain.mothers.account_created_at_primitives_mother import AccountCreatedAtPrimitivesMother
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import AccountPasswordHashPrimitivesMother
from tests.auth.account.domain.mothers.account_status_primitives_mother import AccountStatusPrimitivesMother


class AccountMother(ObjectMother):
    @classmethod
    def any(cls) -> Account:
        return Account(
            id=AccountIdPrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=AccountPasswordHashPrimitivesMother.any(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=AccountCreatedAtPrimitivesMother.any(),
        )
