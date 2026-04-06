from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


# Связующая таблица исполнитель-дисциплина
contractor_disciplines = Table(
    "contractor_disciplines",
    Base.metadata,
    Column("contractor_id", Integer, ForeignKey("contractors.id")),
    Column("discipline_id", Integer, ForeignKey("disciplines.id")),
)


class Contractor(Base):
    __tablename__ = "contractors"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_individual: Mapped[bool] = mapped_column(Boolean, default=True)
    full_name: Mapped[str] = mapped_column(String(255))   # ИП Ершов Дмитрий Игоревич
    short_name: Mapped[str] = mapped_column(String(255))  # Ершов Д.И.
    inn: Mapped[str] = mapped_column(String(12))
    ogrn: Mapped[str] = mapped_column(String(15))
    legal_address: Mapped[str] = mapped_column(String(500))
    bank_name: Mapped[str] = mapped_column(String(255))
    bik: Mapped[str] = mapped_column(String(9))
    account: Mapped[str] = mapped_column(String(20))
    corr_account: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    disciplines: Mapped[list["Discipline"]] = relationship(
        secondary=contractor_disciplines,
        lazy="selectin"
    )