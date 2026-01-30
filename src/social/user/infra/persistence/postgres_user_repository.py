from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.domain.criteria.criteria import Criteria
from src.shared.infra.criteria.criteria_to_sqlalchemy_converter import (
    CriteriaToSqlalchemyConverter,
)
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository
from src.social.user.domain.user_username import UserUsername
from src.social.user.infra.persistence.user_model import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def save(self, user: User) -> None:
        user_to_save = UserModel.from_domain(user)
        await self._session.merge(user_to_save)
        await self._session.flush()

    @override
    async def search(self, username: UserUsername) -> User | None:
        query = select(UserModel).where(UserModel.username == username.value)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user.to_aggregate() if user else None

    @override
    async def matching(self, criteria: Criteria) -> list[User]:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(UserModel, criteria)
        users = await self._session.scalars(query)
        return [user.to_aggregate() for user in users]

    @override
    async def delete(self, username: UserUsername) -> None:
        query = select(UserModel).where(UserModel.username == username.value)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return
        await self._session.delete(user)
        await self._session.flush()
