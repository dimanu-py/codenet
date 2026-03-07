from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from tests.shared.domain.criteria.mothers.expression_mother import CompositeExpressionMother
from tests.shared.domain.criteria.mothers.sorts_mother import SortsMother


class CriteriaMother:
    @staticmethod
    def any() -> Criteria:
        return Criteria(expression=CompositeExpressionMother.any(), sorts=SortsMother.empty())

    @staticmethod
    def empty() -> Criteria:
        return Criteria.from_primitives(expression={})

    @staticmethod
    def with_composite_expression(expression: dict[str, Any]) -> Criteria:
        return Criteria.from_primitives(expression)

    @staticmethod
    def with_comparison_expression(field: str, operator: str, value: str) -> Criteria:
        return Criteria.from_primitives({"field": field, f"{operator}": value})

    @staticmethod
    def with_sorting(sorts: list[dict[str, str]]) -> Criteria:
        return Criteria.from_primitives(expression={}, sorts=sorts)
