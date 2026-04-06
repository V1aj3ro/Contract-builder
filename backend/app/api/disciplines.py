from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contract import Discipline, WorkTemplate
from pydantic import BaseModel

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class DisciplineCreate(BaseModel):
    code: str
    name: str


class WorkCreate(BaseModel):
    text: str


@router.get("/disciplines")
async def get_disciplines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Discipline).options(selectinload(Discipline.works))
    )
    disciplines = result.scalars().all()
    return [
        {
            "id": d.id,
            "code": d.code,
            "name": d.name,
            "works": [{"id": w.id, "text": w.text} for w in d.works],
        }
        for d in disciplines
    ]


@router.post("/disciplines")
async def create_discipline(data: DisciplineCreate, db: AsyncSession = Depends(get_db)):
    discipline = Discipline(**data.model_dump())
    db.add(discipline)
    await db.commit()
    await db.refresh(discipline)
    return {"id": discipline.id, "code": discipline.code}


@router.delete("/disciplines/{discipline_id}")
async def delete_discipline(discipline_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Discipline).where(Discipline.id == discipline_id))
    discipline = result.scalar_one_or_none()
    if not discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    await db.delete(discipline)
    await db.commit()
    return {"ok": True}


@router.post("/disciplines/{discipline_id}/works")
async def add_work(discipline_id: int, data: WorkCreate, db: AsyncSession = Depends(get_db)):
    work = WorkTemplate(discipline_id=discipline_id, text=data.text)
    db.add(work)
    await db.commit()
    await db.refresh(work)
    return {"id": work.id, "text": work.text}


@router.delete("/disciplines/{discipline_id}/works/{work_id}")
async def delete_work(discipline_id: int, work_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WorkTemplate).where(WorkTemplate.id == work_id))
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="Работа не найдена")
    await db.delete(work)
    await db.commit()
    return {"ok": True}