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
