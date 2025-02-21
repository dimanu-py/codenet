from src.shared.domain.criteria.filter_field import FilterField
from tests.social.shared.domain.random_generator import RandomGenerator


class FilterFieldMother:
    @classmethod
    def any(cls) -> FilterField:
        return FilterField(RandomGenerator.word())
