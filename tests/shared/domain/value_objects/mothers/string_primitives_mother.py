from tests.shared.domain.random_generator import RandomGenerator


class StringPrimitivesMother:
    @staticmethod
    def any() -> str:
        return RandomGenerator.word()
