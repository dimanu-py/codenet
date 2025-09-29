from tests.shared.domain.random_generator import RandomGenerator


class UuidPrimitivesMother:
    @staticmethod
    def any() -> str:
        return RandomGenerator.uuid()

    @staticmethod
    def invalid() -> str:
        return "00000000-0000-0000-0000"
