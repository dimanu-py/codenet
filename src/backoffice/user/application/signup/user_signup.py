from src.shared.domain.value_objects.optional import raise_error
from src.backoffice.user.domain.user import User
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.domain.user_username import UserUsername
from tests.backoffice.user.domain.user_already_exists import UsernameAlreadyExists


class UserSignup:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, id: str, name: str, username: str) -> None:
        await self._ensure_user_with_same_username_is_not_signed_up(username)

        user = User(
            id=id,
            name=name,
            username=username,
        )

        await self._store_user(user)

    async def _store_user(self, user: User) -> None:
        await self._repository.save(user)

    async def _ensure_user_with_same_username_is_not_signed_up(self, username: str) -> None:
        already_signed_up_user = await self._repository.search(UserUsername(username))
        already_signed_up_user.match(
            of=lambda _: raise_error(UsernameAlreadyExists()),
            empty=lambda: None,
        )
