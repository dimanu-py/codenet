from enum import StrEnum


class Operator(StrEnum):
    ALL = "all"
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_or_equal"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_or_equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
