from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    users: list[User]

    def __init__(self) -> None:
        self.users = []

    async def save(self, user: User) -> None:
        self.users.append(user)
