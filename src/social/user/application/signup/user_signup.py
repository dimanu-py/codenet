from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository


class UserSignup:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, command: UserSignupCommand) -> None:
        user = User(
            id=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
            password=command.password,
        )

        await self._repository.save(user)
