from src.shared.domain.exceptions.base_error import BaseError


class DomainError(BaseError): ...


class DomainValidationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_type="validation_error")


class ConflictError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_type="conflict_error")


class NotFoundError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_type="not_found_error")
