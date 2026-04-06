from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.contract import Customer
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class CustomerCreate(BaseModel):
    is_individual: bool = False
    full_name: str
    full_name_extended: Optional[str] = None
    short_name: str
    inn: str
    ogrn: str
    kpp: Optional[str] = None
    legal_address: str
    bank_name: str
    bik: str
    account: str
    corr_account: str
    signer_name: str
    signer_name_genitive: Optional[str] = None
    signer_role: Optional[str] = None
    signer_role_nominative: Optional[str] = None


@router.get("/customers")
async def get_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer))
    customers = result.scalars().all()
    return [
        {
            "id": c.id,
            "full_name": c.full_name,
            "inn": c.inn,
            "is_individual": c.is_individual,
        }
        for c in customers
    ]


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Заказчик не найден")
    return customer.__dict__


@router.post("/customers")
async def create_customer(data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    customer = Customer(**data.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return {"id": customer.id, "full_name": customer.full_name}


@router.put("/customers/{customer_id}")
async def update_customer(customer_id: int, data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Заказчик не найден")
    for key, value in data.model_dump().items():
        setattr(customer, key, value)
    await db.commit()
    return {"id": customer.id, "full_name": customer.full_name}