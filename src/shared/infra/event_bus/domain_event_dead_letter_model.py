from datetime import datetime
from typing import Self

from sqlalchemy import UUID, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.infra.event_bus.domain_event_to_consume_model import DomainEventToConsumeModel
from src.shared.infra.persistence.sqlalchemy.base import Base


class DomainEventDeadLetterModel(Base):
    __tablename__ = "domain_events_dead_letter"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    name: Mapped[str] = mapped_column()
    attributes: Mapped[dict] = mapped_column(JSONB)
    attempts: Mapped[int] = mapped_column(Integer, default=1)

    @classmethod
    def from_published_event(cls, event: DomainEventToConsumeModel) -> Self:
        return cls(
            id=event.id,
            occurred_at=event.occurred_at,
            name=event.name,
            attributes=event.attributes,
            attempts=event.attempts,
        )
