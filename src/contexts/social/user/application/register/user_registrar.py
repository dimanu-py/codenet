from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)


class UserRegistrar:
    def __call__(self, command: RegisterUserCommand) -> None:
        raise NotImplementedError
