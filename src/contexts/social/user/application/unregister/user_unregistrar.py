from src.contexts.social.user.domain.user_does_not_exist_error import (
    UserDoesNotExistError,
)
from src.contexts.social.user.domain.user_repository import UserRepository


class UserUnregistrar:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_id: str) -> None:
        await self._ensure_user_exists(user_id)
        await self._repository.delete(user_id)

    async def _ensure_user_exists(self, user_id: str) -> None:
        user = await self._repository.search(user_id)
        if not user:
            raise UserDoesNotExistError
