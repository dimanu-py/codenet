import pytest

from src.shared.infra.persistence.sqlalchemy.session_maker import SessionMaker
from src.shared.infra.settings import Settings
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.user.domain.user_mother import UserMother


@pytest.mark.integration
class TestPostgresUserRepository:
    @classmethod
    def setup_class(cls) -> None:
        cls.session_maker = SessionMaker(settings=Settings())  # type: ignore
        cls.session_maker.create_tables()

    @classmethod
    def teardown_class(cls) -> None:
        with cls.session_maker.get_session() as session:
            session.query(UserModel).delete()
            session.commit()

    @pytest.mark.asyncio
    async def test_should_save_user(self) -> None:
        repository = PostgresUserRepository(session_maker=self.session_maker)
        user = UserMother.any()

        await repository.save(user)
