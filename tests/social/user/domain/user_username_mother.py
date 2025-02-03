from src.social.user.domain.user_username import UserUsername
from tests.social.shared.domain.random_generator import RandomGenerator


class UserUsernameMother:
    @classmethod
    def any(cls) -> UserUsername:
        return UserUsername(RandomGenerator.username())
