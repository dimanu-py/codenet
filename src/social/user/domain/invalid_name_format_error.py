from src.shared.domain.exceptions.domain_error import DomainError


class InvalidNameFormatError(DomainError):
    def __init__(self) -> None:
        self._message = "Name cannot contain special characters or numbers."
        self._type = "invalid_name_format"
        super().__init__(self._message)

    @property
    def type(self) -> str:
        return self._type

    @property
    def message(self) -> str:
        return self._message
