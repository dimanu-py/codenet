from src.social.user.domain.user_repository import UserRepository


class UserSignup:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, id_: str, name: str, username: str, email: str) -> None:
        raise NotImplementedError
