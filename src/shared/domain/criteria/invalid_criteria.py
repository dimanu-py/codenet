from src.shared.domain.exceptions.domain_error import DomainError


class InvalidCriteria(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_type="invalid_structure")


class InvalidCriteriaStructure(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Criteria must be a dictionary")


class InvalidCompositeExpressionStructure(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Logical group filter must contain either 'AND' or 'OR'")


class InvalidExpressionStructure(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Criteria filter expression must contain 'field' or a logical operator 'and/or'")


class MissingFieldInSortCondition(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Missing 'field' in sort condition.")


class MissingDirectionInSortCondition(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Missing 'direction' in sort condition.")


class SortConditionInvalidStructure(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Sort condition has invalid structure. Only 'field' and 'direction' keys are allowed.")
