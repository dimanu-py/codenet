from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from tests.shared.domain.criteria.mothers.expression_mother import LogicalGroupMother


class CriteriaMother:
    @staticmethod
    def any() -> Criteria:
        return Criteria(expression=LogicalGroupMother.any())

    @staticmethod
    def empty() -> Criteria:
        return Criteria.from_primitives(filter_expression={})

    @staticmethod
    def with_conditions(conditions: dict[str, Any]) -> Criteria:
        return Criteria.from_primitives(conditions)

    @staticmethod
    def with_one_condition(field: str, operator: str, value: str) -> Criteria:
        return Criteria.from_primitives({"field": field, f"{operator}": value})
