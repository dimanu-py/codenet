from src.contexts.social.user.domain.user_username import UserUsername
from tests.contexts.shared.domain.random_generator import RandomGenerator


class UserUsernameMother:
    @classmethod
    def create(cls) -> UserUsername:
        return UserUsername(RandomGenerator.username())
