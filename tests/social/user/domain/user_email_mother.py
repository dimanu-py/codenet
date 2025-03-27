from src.social.user.domain.user_email import UserEmail
from tests.social.shared.domain.random_generator import RandomGenerator


class UserEmailMother:
    @staticmethod
    def any() -> UserEmail:
        return UserEmail(RandomGenerator.email())
