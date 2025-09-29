from typing import override

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import (
    CriteriaToSqlalchemyConverter,
)
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.persistence.user_model import UserModel


class PostgresUserRepository(UserRepository):
    _engine: AsyncEngine

    def __init__(self, engine: AsyncEngine, session: AsyncSession | None = None) -> None:
        self._engine = engine
        self._session_maker = async_sessionmaker(bind=self._engine)
        self._session = session

    @override
    async def save(self, user: User) -> None:
        async with self._session_maker() as session:
            user_to_save = UserModel(**user.to_primitives())
            session.add(user_to_save)
            await session.commit()

    @override
    async def find(self, user_id: UserId) -> User | None:
        async with self._session_maker() as session:
            user = await session.get(UserModel, user_id.value)
            return user.to_aggregate() if user else None

    @override
    async def matching(self, criteria: Criteria) -> list[User]:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(UserModel, criteria)
        async with self._session_maker() as session:
            users = await session.scalars(query)
        return [user.to_aggregate() for user in users]

    @override
    async def delete(self, user_id: UserId) -> None:
        async with self._session_maker() as session:
            user = await session.get(UserModel, user_id.value)
            if user:
                await session.delete(user)
                await session.commit()
