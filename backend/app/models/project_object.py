from sqlalchemy import String, Boolean, Date, Table, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime


# Связующая таблица объект-исполнитель
object_contractors = Table(
    "object_contractors",
    Base.metadata,
    Column("object_id", Integer, ForeignKey("project_objects.id")),
    Column("contractor_id", Integer, ForeignKey("contractors.id")),
)


class ProjectObject(Base):
    __tablename__ = "project_objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(500))
    short_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Основание (госконтракт)
    basis_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    basis_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    basis_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    basis_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    basis_object: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    contractors: Mapped[list["Contractor"]] = relationship(
        secondary=object_contractors,
        lazy="selectin"
    )