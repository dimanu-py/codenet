from sindripy.mothers import ObjectMother, StringUuidPrimitivesMother

from src.auth.account.domain.account import Account


class AccountMother(ObjectMother):
    @classmethod
    def any(cls) -> Account:
        return Account(
            id=StringUuidPrimitivesMother.any(),
            email=cls._faker().email(),
            password=cls._faker().password(),
            status="active",
            created_at=cls._faker().date_time(),
        )
