from src.shared.domain.criteria.criteria import Criteria
from tests.social.shared.domain.criteria.filters_mother import FiltersMother


class CriteriaMother:
    @classmethod
    def any(cls) -> Criteria:
        return Criteria(filters=FiltersMother.any())
