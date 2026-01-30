from src.social.user.application.removal.user_not_found_error import UserNotFoundError
from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository


class UserRemover:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, command: UserRemovalCommand) -> None:
        user_id = UserId(command.user_id)
        await self._ensure_user_to_remove_exists(user_id)
        await self._remove_user(user_id)

    async def _remove_user(self, user_id: UserId) -> None:
        return await self._repository.delete(user_id)

    async def _ensure_user_to_remove_exists(self, user_id: UserId) -> None:
        user = await self._repository.search(user_id)
        if not user:
            raise UserNotFoundError()
