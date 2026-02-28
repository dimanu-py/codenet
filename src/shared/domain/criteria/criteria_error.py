from src.shared.domain.exceptions.domain_error import DomainError


class CriteriaError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_type="invalid_structure")


class InvalidCriteriaStructure(CriteriaError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
