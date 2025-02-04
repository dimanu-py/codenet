from src.shared.domain.exceptions.domain_error import DomainError


class InvalidUsernameFormatError(DomainError):
    def __init__(self) -> None:
        self._message = "Username cannot contain special characters"
        self._type = "invalid_username_format"
        super().__init__(self._message)

    @property
    def type(self) -> str:
        return self._type

    @property
    def message(self) -> str:
        return self._message
