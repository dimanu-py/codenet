from datetime import UTC, datetime


class AccountCreatedAtPrimitivesMother:
    @staticmethod
    def dummy() -> datetime:
        return datetime(2026, 11, 7, 15, 30, 0, tzinfo=UTC)
