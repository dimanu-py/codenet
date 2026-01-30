from src.shared.domain.exceptions.base_error import BaseError


class ApplicationError(BaseError):
    """Errors produced by the application layer of the application."""

    ...


class ConflictError(ApplicationError):
    """Errors produced when there is a conflict in the application layer."""

    ...
