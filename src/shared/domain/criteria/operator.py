from enum import StrEnum

from src.shared.domain.criteria.invalid_criteria import InvalidCriteria


class Operator(StrEnum):
    EQUALS = "equals"
    NOT_EQUALS = "does_not_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_or_equal_to"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"


class ComparisonOperatorDoesNotExist(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__("Comparison operator does not exist.")
