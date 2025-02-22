from src.shared.domain.criteria.filters import Filters
from tests.social.shared.domain.criteria.filter_mother import FilterMother


class FiltersMother:
    @classmethod
    def any(cls) -> Filters:
        return Filters([FilterMother.any()])

    @classmethod
    def empty(cls) -> Filters:
        return Filters([])
