from enum import StrEnum
from typing import override

from src.shared.domain.criteria.invalid_criteria import InvalidCriteria


class SortDirection(StrEnum):
    ASCENDING = "ascending"
    DESCENDING = "descending"

    @classmethod
    @override
    def _missing_(cls, value: object) -> None:
        raise SortDirectionDoesNotExist(str(value))


class SortDirectionDoesNotExist(InvalidCriteria):
    def __init__(self, value: str) -> None:
        super().__init__(message=f"Sorting direction '{value}' does not exist.")
