from src.shared.domain.exceptions.domain_error import DomainError


class InvalidIdFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="User id must be a valid UUID",
            error_type="invalid_id_format",
        )
