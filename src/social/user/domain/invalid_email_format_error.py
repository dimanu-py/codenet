from src.shared.domain.exceptions.domain_error import DomainError


class InvalidEmailFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Email cannot contain special characters and must contain '@' and '.'",
            error_type="invalid_email_format",
        )
