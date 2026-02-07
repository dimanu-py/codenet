from sindripy.mothers import ObjectMother

from src.auth.account.domain.account import Account
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_status_primitives_mother import AccountStatusPrimitivesMother


class AccountMother(ObjectMother):
    @classmethod
    def any(cls) -> Account:
        return Account(
            id=AccountIdPrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=cls._faker().password(),
            status=AccountStatusPrimitivesMother.active(),
            created_at=cls._faker().date_time(),
        )
