from src.contexts.social.user.domain.user_repository import UserRepository


class UserUnregistrar:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_id: str) -> None:
        await self._repository.delete(user_id)
