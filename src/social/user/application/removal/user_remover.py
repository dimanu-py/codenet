from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)


class UserRemover:
    _repository: PostgresUserRepository

    def __init__(self, repository: PostgresUserRepository) -> None:
        self._repository = repository

    async def __call__(self, command: UserRemovalCommand) -> None:
        raise NotImplementedError
