from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository
from src.social.user.application.signup.user_signup_command import UserSignupCommand


class UserSignup:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, command: UserSignupCommand) -> None:
        user = User.signup(
            id=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
        )

        await self._repository.save(user)
