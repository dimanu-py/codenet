from src.contexts.social.user.domain.user_id import UserId
from tests.contexts.shared.domain.random_generator import RandomGenerator


class UserIdMother:
    @classmethod
    def create(cls) -> UserId:
        return UserId(RandomGenerator.uuid())
