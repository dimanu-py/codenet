from src.shared.domain.exceptions.domain_error import DomainError


class InvalidNegativeValueError(DomainError):
    def __init__(self, value: int) -> None:
        self._message = f"Invalid negative value: {value}"
        self._type = "invalid_negative_value"
        super().__init__(self._message, self._type)
