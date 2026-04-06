from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contractor import Contractor
from app.models.contractor_work import ContractorWork
from app.models.contract import Discipline, Contract
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


class WorkUpsert(BaseModel):
    text: str


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
        .options(
            selectinload(Contractor.disciplines),
            selectinload(Contractor.works).selectinload(ContractorWork.discipline)
        )
    )
    contractor = result.scalar_one_or_none()
    if not contractor:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")

    # Группируем работы по дисциплинам
    works_by_discipline: dict = {}
    for w in contractor.works:
        did = w.discipline_id
        if did not in works_by_discipline:
            works_by_discipline[did] = []
        works_by_discipline[did].append({"id": w.id, "text": w.text})

    # Активные договоры
    contracts_result = await db.execute(
        select(Contract)
        .where(Contract.contractor_keycloak_id == str(contractor_id))
        .options(selectinload(Contract.customer))
    )
    contracts = contracts_result.scalars().all()

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
        "disciplines": [{"id": d.id, "code": d.code, "name": d.name} for d in contractor.disciplines],
        "works_by_discipline": works_by_discipline,
        "contracts": [
            {
                "id": c.id,
                "number": c.number,
                "date": c.date,
                "object_full_name": c.object_full_name,
                "customer": c.customer.full_name,
                "amount": c.amount,
            }
            for c in contracts
        ],
    }


@router.post("/contractors")
async def create_contractor(data: ContractorCreate, db: AsyncSession = Depends(get_db)):
    discipline_ids = data.discipline_ids
    contractor_data = data.model_dump(exclude={"discipline_ids"})
    contractor = Contractor(**contractor_data)
    if discipline_ids:
        result = await db.execute(select(Discipline).where(Discipline.id.in_(discipline_ids)))
        disciplines = result.scalars().all()
        contractor.disciplines = disciplines
        # Копируем типовые работы из справочника
        for discipline in disciplines:
            works_result = await db.execute(
                select(Discipline).where(Discipline.id == discipline.id)
                .options(selectinload(Discipline.works))
            )
            d = works_result.scalar_one()
            for w in d.works:
                contractor.works.append(
                    ContractorWork(discipline_id=discipline.id, text=w.text)
                )
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


@router.post("/contractors/{contractor_id}/works")
async def add_contractor_work(contractor_id: int, discipline_id: int, data: WorkUpsert, db: AsyncSession = Depends(get_db)):
    work = ContractorWork(contractor_id=contractor_id, discipline_id=discipline_id, text=data.text)
    db.add(work)
    await db.commit()
    await db.refresh(work)
    return {"id": work.id, "text": work.text}


@router.delete("/contractors/{contractor_id}/works/{work_id}")
async def delete_contractor_work(contractor_id: int, work_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContractorWork).where(ContractorWork.id == work_id))
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    await db.delete(work)
    await db.commit()
    return {"ok": True}