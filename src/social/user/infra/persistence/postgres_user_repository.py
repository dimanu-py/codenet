from typing import override

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.value_objects.optional import Optional
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
    async def search(self, username: UserUsername) -> Optional[User]:
        user = await self._session.get(UserModel, username.value)
        return Optional.from_nullable(user).map(lambda u: u.to_domain())

    @override
    async def matching(self, criteria: Criteria) -> list[User]:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(UserModel, criteria)
        users = await self._session.scalars(query)
        return [user.to_domain() for user in users]

    @override
    async def delete(self, username: UserUsername) -> None:
        user = await self._session.get(UserModel, username.value)
        if not user:
            return
        await self._session.delete(user)
        await self._session.flush()
