from src.shared.infra.persistence.sqlalchemy.base import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import mapped_column, Mapped

from src.social.user.domain.user import User


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    def to_aggregate(self) -> User:
        return User.signup(
            id_=str(self.id),
            name=self.name,
            username=self.username,
            email=self.email,
        )
