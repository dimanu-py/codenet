from enum import StrEnum
from typing import override

from src.shared.domain.exceptions.domain_error import DomainValidationError


class AccountStatus(StrEnum):
    ACTIVE = "active"

    @classmethod
    def default(cls) -> str:
        return cls.ACTIVE

    @classmethod
    @override
    def _missing_(cls, value: object) -> None:
        raise AccountStatusDoesNotExists(str(value))


class AccountStatusDoesNotExists(DomainValidationError):
    def __init__(self, status: str) -> None:
        super().__init__(
            message=f"Account status '{status}' does not exist.",
            error_type="account_validation_error",
        )
