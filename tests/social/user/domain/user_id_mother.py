from src.social.user.domain.user_id import UserId
from tests.social.shared.domain.random_generator import RandomGenerator


class UserIdMother:
    @classmethod
    def any(cls) -> UserId:
        return UserId(RandomGenerator.uuid())
