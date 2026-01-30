from src.social.user.application.signup.user_signup_command import UserSignupCommand
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository
from src.social.user.domain.user_username import UserUsername
from tests.social.user.domain.user_already_exists import UsernameAlreadyExists


class UserSignup:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, command: UserSignupCommand) -> None:
        await self._ensure_user_with_same_username_is_not_signed_up(command.username)

        user = User(
            id=command.id,
            name=command.name,
            username=command.username,
            email=command.email,
            password=command.password,
        )

        await self._store_user(user)

    async def _store_user(self, user: User) -> None:
        await self._repository.save(user)

    async def _ensure_user_with_same_username_is_not_signed_up(self, username: str) -> None:
        already_signed_up_user = await self._repository.search(UserUsername(username))
        if already_signed_up_user:
            raise UsernameAlreadyExists
