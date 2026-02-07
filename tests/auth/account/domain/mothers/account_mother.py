from sindripy.mothers import ObjectMother, StringUuidPrimitivesMother

from src.auth.account.domain.account import Account
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother


class AccountMother(ObjectMother):
    @classmethod
    def any(cls) -> Account:
        return Account(
            id=StringUuidPrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=cls._faker().password(),
            status="active",
            created_at=cls._faker().date_time(),
        )
