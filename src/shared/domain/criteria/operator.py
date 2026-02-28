from enum import StrEnum


class Operator(StrEnum):
    EQUAL = "equals"
    NOT_EQUAL = "does_not_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_or_equal_to"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
