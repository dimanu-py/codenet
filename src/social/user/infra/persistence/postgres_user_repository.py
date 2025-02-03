from typing import override

from src.shared.infra.persistence.sqlalchemy.session_maker import SessionMaker
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.persistence.user_model import UserModel


class PostgresUserRepository(UserRepository):
    _session_maker: SessionMaker

    def __init__(self, session_maker: SessionMaker) -> None:
        self._session_maker = session_maker

    @override
    async def save(self, user: User) -> None:
        async with self._session_maker.get_session() as session:
            user_to_save = UserModel(**user.to_dict())
            session.add(user_to_save)
            await session.commit()

