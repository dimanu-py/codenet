from src.shared.domain.exceptions.domain_error import DomainError


class InvalidUsernameFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Username cannot contain special characters",
            error_type="invalid_username_format",
        )
