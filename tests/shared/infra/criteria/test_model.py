from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.infra.persistence.sqlalchemy.base import Base


class TestModel(Base):
    __tablename__ = "test_table"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
