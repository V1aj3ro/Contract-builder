from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contractor import Contractor
from app.models.contract import Discipline
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class ContractorCreate(BaseModel):
    is_individual: bool = True
    full_name: str
    short_name: str
    inn: str
    ogrn: str
    legal_address: str
    bank_name: str
    bik: str
    account: str
    corr_account: str
    phone: Optional[str] = None
    discipline_ids: list[int] = []


@router.get("/contractors")
async def get_contractors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contractor)
        .where(Contractor.is_active == True)
        .options(selectinload(Contractor.disciplines))
    )
    contractors = result.scalars().all()
    return [
        {
            "id": c.id,
            "full_name": c.full_name,
            "short_name": c.short_name,
            "inn": c.inn,
            "is_individual": c.is_individual,
            "phone": c.phone,
            "disciplines": [{"id": d.id, "code": d.code, "name": d.name} for d in c.disciplines],
        }
        for c in contractors
    ]


@router.get("/contractors/{contractor_id}")
async def get_contractor(contractor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contractor)
        .where(Contractor.id == contractor_id)
        .options(selectinload(Contractor.disciplines))
    )
    contractor = result.scalar_one_or_none()
    if not contractor:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    return {
        "id": contractor.id,
        "is_individual": contractor.is_individual,
        "full_name": contractor.full_name,
        "short_name": contractor.short_name,
        "inn": contractor.inn,
        "ogrn": contractor.ogrn,
        "legal_address": contractor.legal_address,
        "bank_name": contractor.bank_name,
        "bik": contractor.bik,
        "account": contractor.account,
        "corr_account": contractor.corr_account,
        "phone": contractor.phone,
        "discipline_ids": [d.id for d in contractor.disciplines],
    }


@router.post("/contractors")
async def create_contractor(data: ContractorCreate, db: AsyncSession = Depends(get_db)):
    discipline_ids = data.discipline_ids
    contractor_data = data.model_dump(exclude={"discipline_ids"})
    contractor = Contractor(**contractor_data)
    if discipline_ids:
        result = await db.execute(select(Discipline).where(Discipline.id.in_(discipline_ids)))
        contractor.disciplines = result.scalars().all()
    db.add(contractor)
    await db.commit()
    await db.refresh(contractor)
    return {"id": contractor.id, "full_name": contractor.full_name}


@router.put("/contractors/{contractor_id}")
async def update_contractor(contractor_id: int, data: ContractorCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contractor)
        .where(Contractor.id == contractor_id)
        .options(selectinload(Contractor.disciplines))
    )
    contractor = result.scalar_one_or_none()
    if not contractor:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    discipline_ids = data.discipline_ids
    for key, value in data.model_dump(exclude={"discipline_ids"}).items():
        setattr(contractor, key, value)
    if discipline_ids is not None:
        result = await db.execute(select(Discipline).where(Discipline.id.in_(discipline_ids)))
        contractor.disciplines = result.scalars().all()
    await db.commit()
    return {"id": contractor.id, "full_name": contractor.full_name}


@router.delete("/contractors/{contractor_id}")
async def deactivate_contractor(contractor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contractor).where(Contractor.id == contractor_id))
    contractor = result.scalar_one_or_none()
    if not contractor:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    contractor.is_active = False
    await db.commit()
    return {"ok": True}