from datetime import UTC, datetime

from object_mother import ObjectMother


class AccountCreatedAtPrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> datetime:
        return cls._faker().date_time(tzinfo=UTC)

    @classmethod
    def dummy(cls) -> datetime:
        return datetime(2026, 11, 7, 15, 30, 0, tzinfo=UTC)
