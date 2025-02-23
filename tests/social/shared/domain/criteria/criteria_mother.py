from src.shared.domain.criteria.criteria import Criteria
from tests.social.shared.domain.criteria.filters_mother import FiltersMother


class CriteriaMother:
    @classmethod
    def any(cls) -> Criteria:
        return Criteria(filters=FiltersMother.any())

    @classmethod
    def with_one_filter(cls, field: str, operator: str, value: str) -> Criteria:
        return Criteria.from_primitives(
            [{"field": field, "operator": operator, "value": value}]
        )

    @classmethod
    def empty(cls) -> Criteria:
        return Criteria(filters=FiltersMother.empty())

    @classmethod
    def create(cls, fixed_filters: list[dict]) -> Criteria:
        return Criteria.from_primitives(fixed_filters)
