from src.shared.domain.criteria.condition.field import Field
from tests.social.shared.domain.random_generator import RandomGenerator


class FieldMother:
    @staticmethod
    def any() -> Field:
        return Field(RandomGenerator.word())
