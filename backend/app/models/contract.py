from sqlalchemy import String, Date, Numeric, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime
import decimal


class Customer(Base):
    """Заказчик — ООО или ИП"""
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_individual: Mapped[bool] = mapped_column(Boolean, default=False)  # True = ИП
    full_name: Mapped[str] = mapped_column(String(255))   # ООО «Знамя архитектуры»
    short_name: Mapped[str] = mapped_column(String(255))  # Знамя архитектуры
    inn: Mapped[str] = mapped_column(String(12))
    ogrn: Mapped[str] = mapped_column(String(15))
    kpp: Mapped[str | None] = mapped_column(String(9), nullable=True)  # нет у ИП
    legal_address: Mapped[str] = mapped_column(String(500))
    bank_name: Mapped[str] = mapped_column(String(255))
    bik: Mapped[str] = mapped_column(String(9))
    account: Mapped[str] = mapped_column(String(20))
    corr_account: Mapped[str] = mapped_column(String(20))
    signer_name: Mapped[str] = mapped_column(String(255))  # Дьяченко О.Н.
    signer_role: Mapped[str | None] = mapped_column(String(100), nullable=True)  # директор

    contracts: Mapped[list["Contract"]] = relationship(back_populates="customer")


class Discipline(Base):
    """Дисциплина — АР, КР, ТМ и т.д."""
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True)  # АР
    name: Mapped[str] = mapped_column(String(255))              # Архитектурные решения

    works: Mapped[list["WorkTemplate"]] = relationship(back_populates="discipline")


class WorkTemplate(Base):
    """Типовая работа для дисциплины"""
    __tablename__ = "work_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    text: Mapped[str] = mapped_column(Text)  # описание работы

    discipline: Mapped["Discipline"] = relationship(back_populates="works")


class Contract(Base):
    """Договор подряда"""
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(50))
    date: Mapped[datetime.date] = mapped_column(Date)
    city: Mapped[str] = mapped_column(String(100), default="г. Новосибирск")

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contracts")

    # Исполнитель — keycloak_id + кэш реквизитов на момент создания договора
    contractor_keycloak_id: Mapped[str] = mapped_column(String(100))
    contractor_full_name: Mapped[str] = mapped_column(String(255))
    contractor_inn: Mapped[str] = mapped_column(String(12))
    contractor_ogrn: Mapped[str] = mapped_column(String(15))
    contractor_is_individual: Mapped[bool] = mapped_column(Boolean, default=True)
    contractor_legal_address: Mapped[str] = mapped_column(String(500))
    contractor_bank_name: Mapped[str] = mapped_column(String(255))
    contractor_bik: Mapped[str] = mapped_column(String(9))
    contractor_account: Mapped[str] = mapped_column(String(20))
    contractor_corr_account: Mapped[str] = mapped_column(String(20))

    # Объект
    object_full_name: Mapped[str] = mapped_column(String(500))
    object_address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Основание (госконтракт)
    basis_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    basis_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    basis_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    basis_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    # Сроки
    date_start: Mapped[datetime.date] = mapped_column(Date)
    date_end: Mapped[datetime.date] = mapped_column(Date)

    # Сумма
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2))
    vat_included: Mapped[bool] = mapped_column(Boolean, default=False)

    # Транши
    tranch1_pct: Mapped[int] = mapped_column(Integer, default=30)
    tranch1_condition: Mapped[str] = mapped_column(String(500))
    tranch2_pct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tranch2_condition: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tranch3_pct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tranch3_condition: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Доп. условия
    extra_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)

    works_text: Mapped[str] = mapped_column(Text)  # итоговый текст объёма работ