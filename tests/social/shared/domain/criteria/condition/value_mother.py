from src.shared.domain.criteria.condition.value import Value
from tests.social.shared.domain.random_generator import RandomGenerator


class ValueMother:
    @staticmethod
    def any() -> Value:
        return Value(RandomGenerator.word())
