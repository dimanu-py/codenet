from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository


class UserRemover:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, command: UserRemovalCommand) -> None:
        existing_user = await self._ensure_user_to_remove_exists(command.user_id)
        await self._repository.delete(existing_user)

    async def _ensure_user_to_remove_exists(self, user_id: str) -> User:
        user = await self._repository.find(UserId(user_id))
        if not user:
            raise UserNotFoundError(user_id)
