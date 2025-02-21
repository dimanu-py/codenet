from typing import override

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.persistence.user_model import UserModel


class PostgresUserRepository(UserRepository):
    _engine: AsyncEngine

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._session_maker = async_sessionmaker(bind=self._engine)

    @override
    async def save(self, user: User) -> None:
        async with self._session_maker() as session:
            user_to_save = UserModel(**user.to_dict())
            session.add(user_to_save)
            await session.commit()

    @override
    async def search(self, user_id: UserId) -> User | None:
        async with self._session_maker() as session:
            user = await session.get(UserModel, user_id.value)
            return user.to_aggregate() if user else None

    @override
    async def matching(self, criteria: Criteria) -> list[User] | None:
        raise NotImplementedError
