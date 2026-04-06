from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models.contract import Contract
from app.schemas.contract import ContractCreate
from app.services.generator import generate_contract

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


@router.get("/contracts/{contract_id}/generate")
async def generate(contract_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Contract)
        .options(selectinload(Contract.customer))
        .where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")

    docx_bytes = generate_contract(contract, contract.customer)

    filename = f"contract_{contract.number.replace('/', '-')}.docx"
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )