from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.auth.account.domain.account import Account
from src.shared.infra.persistence.sqlalchemy.base import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @classmethod
    def from_domain(cls, account: Account) -> Self:
        return cls(**account.to_primitives())

    def to_domain(self) -> Account:
        return Account(
            id=self.id,
            email=self.email,
            password=self.password,
            status=self.status,
            created_at=self.created_at,
        )