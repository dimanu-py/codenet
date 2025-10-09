from typing import Self

from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import HealthcheckWaitStrategy


class PostgresTestContainer(DockerContainer):
    _POSTGRES_IMAGE = "postgres:17"
    _PORT = 5432
    _USER = "test_user"
    _PASSWORD = "test_password"
    _DATABASE_NAME = "test_db"
    _HEALTHCHECK_INTERVAL_SECONDS = 1
    _HEALTHCHECK_TIMEOUT_SECONDS = 3
    _HEALTHCHECK_RETRIES_LIMIT = 5
    _HEALTHCHECK_START_PERIOD_SECONDS = 5
    _TO_NANOSECONDS = 1_000_000_000

    def __init__(self) -> None:
        super().__init__(self._POSTGRES_IMAGE)
        self.with_exposed_ports(self._PORT)
        self.with_env("POSTGRES_DB", self._DATABASE_NAME)
        self.with_env("POSTGRES_USER", self._USER)
        self.with_env("POSTGRES_PASSWORD", self._PASSWORD)
        self.with_kwargs(
            healthcheck={
                "test": ["CMD-SHELL", f"pg_isready -U {self._USER} -d {self._DATABASE_NAME}"],
                "interval": self._HEALTHCHECK_INTERVAL_SECONDS * self._TO_NANOSECONDS,
                "timeout": self._HEALTHCHECK_TIMEOUT_SECONDS * self._TO_NANOSECONDS,
                "retries": self._HEALTHCHECK_RETRIES_LIMIT,
                "start_period": self._HEALTHCHECK_START_PERIOD_SECONDS * self._TO_NANOSECONDS,
            }
        )
        self.wait_strategy = HealthcheckWaitStrategy()

    def start(self) -> Self:
        super().start()
        self.wait_strategy.wait_until_ready(self)
        return self

    def get_base_url(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self._PORT)
        return f"postgresql+asyncpg://{self._USER}:{self._PASSWORD}@{host}:{port}/{self._DATABASE_NAME}"
