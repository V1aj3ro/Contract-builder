from fastapi import FastAPI
from app.api.customers import router as customers_router
from app.api.disciplines import router as disciplines_router
from app.api.contracts import router as contracts_router

app = FastAPI(title="Contract Builder")

app.include_router(customers_router, prefix="/api")
app.include_router(disciplines_router, prefix="/api")
app.include_router(contracts_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok"}