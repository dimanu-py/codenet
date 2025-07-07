from src.shared.domain.exceptions.domain_error import DomainError


class RequiredValueError(DomainError):
    def __init__(self) -> None:
        self._message = "Value is required, can't be None"
        self._type = "required_value"
        super().__init__(self._message, self._type)
