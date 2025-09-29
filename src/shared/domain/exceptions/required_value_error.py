from src.shared.domain.exceptions.domain_error import DomainError


class RequiredValueError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Value is required, can't be None",
            error_type="required_value",
        )
