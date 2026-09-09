from typing import Any

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filters_to_criteria_converter import FiltersToCriteriaConverter
from src.shared.domain.criteria.filter import Filters
from tests.shared.domain.criteria.mothers.filter_mother import FilterMother


class CriteriaMother:
    @staticmethod
    def any() -> Criteria:
        return Criteria(filters=Filters([FilterMother.any()]))

    @staticmethod
    def empty() -> Criteria:
        return Criteria.empty()

    @staticmethod
    def with_multiple_filters(expression: dict[str, Any]) -> Criteria:
        return FiltersToCriteriaConverter.convert(filters=expression)

    @staticmethod
    def with_single_filter(field: str, operator: str, value: str) -> Criteria:
        return FiltersToCriteriaConverter.convert(filters={"field": field, f"{operator}": value})

    @staticmethod
    def with_sorting(sorts: list[dict[str, str]]) -> Criteria:
        return FiltersToCriteriaConverter.convert(filters={}, sorts=sorts)
