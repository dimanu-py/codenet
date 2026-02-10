from datetime import datetime
from typing import Self

from sqlalchemy import UUID, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.domain.event_bus.domain_event import DomainEvent
from src.shared.infra.persistence.sqlalchemy.base import Base


class DomainEventToConsumeModel(Base):
    __tablename__ = "domain_events_to_consume"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    type: Mapped[str] = mapped_column()
    attributes: Mapped[dict] = mapped_column(JSONB)

    @classmethod
    def from_domain(cls, event: DomainEvent) -> Self:
        return cls(**event.to_primitives())
