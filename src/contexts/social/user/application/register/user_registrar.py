from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_repository import UserRepository


class UserRegistrar:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, command: RegisterUserCommand) -> None:
        user = User.create(
            id_=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
            profile_picture=command.profile_picture,
        )

        await self._repository.save(user)
