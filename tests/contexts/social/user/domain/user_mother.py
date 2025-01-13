from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.domain.user import User


class UserMother:
    @classmethod
    def from_command(cls, command: RegisterUserCommand) -> User:
        return User.create(
            id_=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
            profile_picture=command.profile_picture,
        )
