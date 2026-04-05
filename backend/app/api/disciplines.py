from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contract import Discipline

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


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