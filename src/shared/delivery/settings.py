from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"), extra="ignore")
    postgres_user: str = Field(default="postgres", alias="POSTGRES_USER")
    postgres_password: str = Field(default="postgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="postgres", alias="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: str = Field(default="5432", alias="POSTGRES_PORT")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")
    jwt_expires_in: int = Field(alias="JWT_EXPIRES_IN")

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @field_validator("jwt_expires_in")
    @classmethod
    def validate_jwt_expires_in(cls, expires_in: int) -> int:
        if expires_in <= 0:
            raise ValueError("jwt_expires_in must be a positive integer")
        return expires_in
