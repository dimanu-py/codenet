from src.social.user.domain.user_name import UserName
from tests.social.shared.domain.random_generator import RandomGenerator


class UserNameMother:
    @classmethod
    def any(cls) -> UserName:
        return UserName(RandomGenerator.name())
