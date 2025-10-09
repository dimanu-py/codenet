from typing import Self

from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy


class PostgresTestContainer(DockerContainer):
    _POSTGRES_IMAGE = "postgres:17"
    _PORT = 5432
    _USER = "test_user"
    _PASSWORD = "test_password"
    _DATABASE_NAME = "test_db"

    def __init__(self) -> None:
        super().__init__(self._POSTGRES_IMAGE)
        self.with_exposed_ports(self._PORT)
        self.with_env("POSTGRES_DB", self._DATABASE_NAME)
        self.with_env("POSTGRES_USER", self._USER)
        self.with_env("POSTGRES_PASSWORD", self._PASSWORD)
        self.waiting_for(LogMessageWaitStrategy("database system is ready to accept connections"))

    def start(self) -> Self:
        super().start()
        return self

    def get_base_url(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self._PORT)
        return f"postgresql+asyncpg://{self._USER}:{self._PASSWORD}@{host}:{port}/{self._DATABASE_NAME}"
