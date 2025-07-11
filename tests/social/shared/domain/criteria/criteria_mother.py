from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from tests.social.shared.domain.criteria.nested_logical_condition_mother import (
    NestedLogicalConditionMother,
)


class CriteriaMother:
    @staticmethod
    def any() -> Criteria:
        return Criteria(expression=NestedLogicalConditionMother.any())

    @staticmethod
    def empty() -> Criteria:
        return Criteria.from_primitives(filter_expression={})

    @staticmethod
    def create(fixed_filters: dict[str, Any]) -> Criteria:
        return Criteria.from_primitives(fixed_filters)

    @staticmethod
    def with_one_filter(field: str, operator: str, value: str) -> Criteria:
        return Criteria.from_primitives({"field": field, f"{operator}": value})
