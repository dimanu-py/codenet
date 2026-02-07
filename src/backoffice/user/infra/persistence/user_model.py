from typing import Self

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.backoffice.user.domain.user import User
from src.shared.infra.persistence.sqlalchemy.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("accounts.id"))
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, primary_key=True)

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(**user.to_primitives())

    def to_domain(self) -> User:
        return User(
            id=str(self.id),
            name=self.name,
            username=self.username,
        )
