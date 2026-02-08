from src.backoffice.user.application.removal.user_not_found import UserNotFound
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.domain.user_username import UserUsername
from src.shared.domain.value_objects.optional import raise_error


class UserRemover:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, username: str) -> None:
        user_username = UserUsername(username)
        await self._ensure_user_to_remove_exists(user_username)
        await self._remove_user(user_username)

    async def _remove_user(self, username: UserUsername) -> None:
        return await self._repository.delete(username)

    async def _ensure_user_to_remove_exists(self, username: UserUsername) -> None:
        user = await self._repository.search(username)
        user.match(
            of=lambda _: None,
            empty=lambda: raise_error(UserNotFound()),
        )
