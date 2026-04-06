from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.project_object import ProjectObject
from app.models.contractor import Contractor
from pydantic import BaseModel
from typing import Optional
import datetime

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class ObjectCreate(BaseModel):
    full_name: str
    short_name: str
    address: Optional[str] = None
    basis_enabled: bool = False
    basis_type: Optional[str] = None
    basis_number: Optional[str] = None
    basis_date: Optional[datetime.date] = None
    basis_object: Optional[str] = None


@router.get("/objects")
async def get_objects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectObject)
        .where(ProjectObject.is_active == True)
        .options(selectinload(ProjectObject.contractors))
    )
    objects = result.scalars().all()
    return [
        {
            "id": o.id,
            "full_name": o.full_name,
            "short_name": o.short_name,
            "address": o.address,
            "basis_enabled": o.basis_enabled,
            "basis_type": o.basis_type,
            "basis_number": o.basis_number,
            "basis_date": o.basis_date,
            "contractors": [{"id": c.id, "full_name": c.full_name} for c in o.contractors],
        }
        for o in objects
    ]


@router.get("/objects/{object_id}")
async def get_object(object_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectObject)
        .where(ProjectObject.id == object_id)
        .options(selectinload(ProjectObject.contractors).selectinload(Contractor.disciplines))
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    return {
        "id": obj.id,
        "full_name": obj.full_name,
        "short_name": obj.short_name,
        "address": obj.address,
        "basis_enabled": obj.basis_enabled,
        "basis_type": obj.basis_type,
        "basis_number": obj.basis_number,
        "basis_date": obj.basis_date,
        "basis_object": obj.basis_object,
        "contractors": [
            {
                "id": c.id,
                "full_name": c.full_name,
                "inn": c.inn,
                "phone": c.phone,
                "disciplines": [{"id": d.id, "code": d.code} for d in c.disciplines],
            }
            for c in obj.contractors
        ],
    }


@router.post("/objects")
async def create_object(data: ObjectCreate, db: AsyncSession = Depends(get_db)):
    obj = ProjectObject(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return {"id": obj.id, "full_name": obj.full_name}


@router.put("/objects/{object_id}")
async def update_object(object_id: int, data: ObjectCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectObject).where(ProjectObject.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    return {"id": obj.id, "full_name": obj.full_name}


@router.delete("/objects/{object_id}")
async def delete_object(object_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectObject).where(ProjectObject.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    obj.is_active = False
    await db.commit()
    return {"ok": True}


@router.post("/objects/{object_id}/contractors/{contractor_id}")
async def add_contractor_to_object(object_id: int, contractor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectObject)
        .where(ProjectObject.id == object_id)
        .options(selectinload(ProjectObject.contractors))
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    contractor_result = await db.execute(select(Contractor).where(Contractor.id == contractor_id))
    contractor = contractor_result.scalar_one_or_none()
    if not contractor:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    obj.contractors.append(contractor)
    await db.commit()
    return {"ok": True}


@router.delete("/objects/{object_id}/contractors/{contractor_id}")
async def remove_contractor_from_object(object_id: int, contractor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectObject)
        .where(ProjectObject.id == object_id)
        .options(selectinload(ProjectObject.contractors))
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    obj.contractors = [c for c in obj.contractors if c.id != contractor_id]
    await db.commit()
    return {"ok": True}