from src.shared.domain.exceptions.domain_error import DomainError


class InvalidNameFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Name cannot contain special characters or numbers.",
            error_type="invalid_name_format",
        )
