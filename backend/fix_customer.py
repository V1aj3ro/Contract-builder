import asyncio
from app.database import AsyncSessionLocal
from app.models.contract import Customer
from sqlalchemy import select

async def fix():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Customer).where(Customer.id == 1))
        customer = result.scalar_one()
        customer.full_name_extended = 'Общество с ограниченной ответственностью «Знамя архитектуры»'
        await session.commit()
        print(f"Updated: {customer.full_name_extended}")

if __name__ == "__main__":
    asyncio.run(fix())