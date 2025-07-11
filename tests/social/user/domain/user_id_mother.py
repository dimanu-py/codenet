from src.social.user.domain.user_id import UserId
from tests.shared.domain.random_generator import RandomGenerator


class UserIdMother:
    @staticmethod
    def any() -> UserId:
        return UserId(RandomGenerator.uuid())
