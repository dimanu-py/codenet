from sindripy.value_objects import SindriValidationError

from src.shared.domain.exceptions.base_error import BaseError


class DomainError(BaseError, SindriValidationError):
    """Errors produced by the domain layer of the application."""

    ...
