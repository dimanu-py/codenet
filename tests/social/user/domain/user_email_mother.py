from src.social.user.domain.user_email import UserEmail
from tests.social.shared.domain.random_generator import RandomGenerator


class UserEmailMother:
    @classmethod
    def any(cls) -> UserEmail:
        return UserEmail(RandomGenerator.email())
