from src.social.user.domain.user_username import UserUsername
from tests.shared.domain.random_generator import RandomGenerator


class UserUsernameMother:
    @staticmethod
    def any() -> UserUsername:
        return UserUsername(RandomGenerator.username())
