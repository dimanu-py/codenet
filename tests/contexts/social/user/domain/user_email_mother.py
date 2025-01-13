from src.contexts.social.user.domain.user_email import UserEmail
from tests.contexts.shared.domain.random_generator import RandomGenerator


class UserEmailMother:
    @classmethod
    def create(cls) -> UserEmail:
        return UserEmail(RandomGenerator.email())
