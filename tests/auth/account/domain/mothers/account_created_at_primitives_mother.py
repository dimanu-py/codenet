from datetime import datetime, timezone

from sindripy.mothers import ObjectMother


class AccountCreatedAtPrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> datetime:
        return cls._faker().date_time(tzinfo=timezone.utc)
