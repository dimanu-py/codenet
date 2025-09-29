from src.social.user.application.removal.user_removal_command import UserRemovalCommand


class UserRemovalCommandMother:

    @classmethod
    def with_id(cls, user_id: str) -> UserRemovalCommand:
        return UserRemovalCommand(
            user_id=user_id,
        )
