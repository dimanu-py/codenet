from typing import Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.infra.persistence.sqlalchemy.base import Base
from src.social.user.domain.user import User


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String)

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(**user.to_primitives())

    def to_aggregate(self) -> User:
        return User(
            id=str(self.id),
            name=self.name,
            username=self.username,
            email=self.email,
            password=self.password,
        )
