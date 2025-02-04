from src.shared.domain.exceptions.domain_error import DomainError


class InvalidEmailFormatError(DomainError):
    def __init__(self) -> None:
        self._message = (
            "Email cannot contain special characters and must contain '@' and '.'"
        )
        self._type = "invalid_email_format"
        super().__init__(self._message)

    @property
    def type(self) -> str:
        return self._type

    @property
    def message(self) -> str:
        return self._message
