from datetime import datetime, timedelta

from sindripy.value_objects import SindriValidationError, ValueObject

from src.shared.domain.value_objects.validation import validate


class AccountCreatedAt(ValueObject[datetime]):
    @validate
    def _ensure_has_value(self) -> None:
        if self._value is None:
            raise SindriValidationError(message="Value is required, can't be None")

    @validate
    def _ensure_is_datetime(self) -> None:
        if not isinstance(self._value, datetime):
            raise SindriValidationError(
                message=f"Value '{self._value}' is not of type {datetime.__name__}",
            )

    @validate
    def _ensure_has_utc_timezone(self) -> None:
        if self._value.tzinfo is None or self._value.tzinfo.utcoffset(self._value) != timedelta(0):
            raise SindriValidationError(
                message=f"Value '{self._value}' must have UTC timezone",
            )
