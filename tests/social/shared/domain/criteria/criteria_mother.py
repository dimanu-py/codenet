from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from tests.social.shared.domain.criteria.filter_expression_mother import FilterExpressionMother


class CriteriaMother:
    @staticmethod
    def any() -> Criteria:
        return Criteria(expression=FilterExpressionMother.any())

    @staticmethod
    def empty() -> Criteria:
        return Criteria.from_primitives(filter_expression={})

    @staticmethod
    def create(fixed_filters: dict[str, Any]) -> Criteria:
        return Criteria.from_primitives(fixed_filters)

    @staticmethod
    def with_one_filter(field: str, operator: str, value: str) -> Criteria:
        return Criteria.from_primitives({"field": field, "operator": operator, "value": value})
