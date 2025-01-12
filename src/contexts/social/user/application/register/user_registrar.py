from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.domain.user_repository import UserRepository


class UserRegistrar:
    _repository: UserRepository | None

    def __init__(self, repository: UserRepository | None = None) -> None:
        self._repository = repository

    def __call__(self, command: RegisterUserCommand) -> None:
        raise NotImplementedError
