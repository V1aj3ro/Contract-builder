from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contract import Contract
from app.schemas.contract import ContractCreate

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/contracts")
async def get_contracts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contract).options(selectinload(Contract.customer))
    )
    contracts = result.scalars().all()
    return [
        {
            "id": c.id,
            "number": c.number,
            "date": c.date,
            "object_full_name": c.object_full_name,
            "contractor_full_name": c.contractor_full_name,
            "customer": c.customer.full_name,
            "amount": c.amount,
        }
        for c in contracts
    ]


@router.post("/contracts")
async def create_contract(data: ContractCreate, db: AsyncSession = Depends(get_db)):
    contract = Contract(**data.model_dump())
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return {"id": contract.id, "number": contract.number}