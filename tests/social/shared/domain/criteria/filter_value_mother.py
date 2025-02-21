from src.shared.domain.criteria.filter_value import FilterValue
from tests.social.shared.domain.random_generator import RandomGenerator


class FilterValueMother:
    @classmethod
    def any(cls) -> FilterValue:
        return FilterValue(RandomGenerator.word())
