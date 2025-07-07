from src.shared.domain.exceptions.domain_error import DomainError


class InvalidIdFormatError(DomainError):
    def __init__(self) -> None:
        self._message = "User id must be a valid UUID"
        self._type = "invalid_id_format"
        super().__init__(self._message, self._type)
