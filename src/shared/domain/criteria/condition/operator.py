from enum import StrEnum


class Operator(StrEnum):
    ALL = "all"
    EQUAL = "eq"
    NOT_EQUAL = "neq"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
