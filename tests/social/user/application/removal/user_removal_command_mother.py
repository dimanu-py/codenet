from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from tests.social.user.domain.user_id_mother import UserIdMother


class UserRemovalCommandMother:
    @staticmethod
    def any() -> UserRemovalCommand:
        return UserRemovalCommand(
            user_id=UserIdMother.any().value,
        )

    @classmethod
    def create(cls, **overrides) -> UserRemovalCommand:
        defaults = cls.any().to_primitives()
        defaults.update(overrides)
        return UserRemovalCommand(**defaults)
