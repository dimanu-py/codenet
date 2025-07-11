from tests.shared.domain.random_generator import RandomGenerator


class IntPrimitivesMother:
    @staticmethod
    def any() -> int:
        return RandomGenerator.positive_integer()
