from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src.shared.infra.persistence.sqlalchemy.base import (
    Base,
)

from src.shared.infra.settings import Settings


class SessionMaker:
    _session_maker: sessionmaker[Session]
    _engine: Engine

    def __init__(self, settings: Settings) -> None:
        self._engine = create_engine(settings.postgres_url)
        self._session_maker = sessionmaker(bind=self._engine)

    def get_session(self) -> Session:
        return self._session_maker()

    def create_tables(self) -> None:
        Base.metadata.create_all(self._engine)
