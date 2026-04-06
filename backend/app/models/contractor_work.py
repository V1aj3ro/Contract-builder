from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ContractorWork(Base):
    __tablename__ = "contractor_works"

    id: Mapped[int] = mapped_column(primary_key=True)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractors.id"))
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    text: Mapped[str] = mapped_column(Text)

    contractor: Mapped["Contractor"] = relationship(back_populates="works")
    discipline: Mapped["Discipline"] = relationship()