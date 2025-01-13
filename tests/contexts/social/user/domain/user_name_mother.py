from src.contexts.social.user.domain.user_name import UserName
from tests.contexts.shared.domain.random_generator import RandomGenerator


class UserNameMother:
    @classmethod
    def create(cls) -> UserName:
        return UserName(RandomGenerator.name())
