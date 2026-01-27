from typing import override

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
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def save(self, user: User) -> None:
        user_to_save = UserModel(**user.to_primitives())
        self._session.add(user_to_save)
        await self._session.flush()

    @override
    async def find(self, user_id: UserId) -> User | None:
        user = await self._session.get(UserModel, user_id.value)
        return user.to_aggregate() if user else None

    @override
    async def matching(self, criteria: Criteria) -> list[User]:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(UserModel, criteria)
        users = await self._session.scalars(query)
        return [user.to_aggregate() for user in users]

    @override
    async def delete(self, user_id: UserId) -> None:
        user = await self._session.get(UserModel, user_id.value)
        if user:
            await self._session.delete(user)
            await self._session.flush()
