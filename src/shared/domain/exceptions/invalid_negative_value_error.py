from src.shared.domain.exceptions.domain_error import DomainError


class InvalidNegativeValueError(DomainError):
    def __init__(self, value: int) -> None:
        super().__init__(
            message=f"Invalid negative value: {value}",
            error_type="invalid_negative_value",
        )
