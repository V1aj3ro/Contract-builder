from fastapi import FastAPI
from app.api.customers import router as customers_router

app = FastAPI(title="Contract Builder")

app.include_router(customers_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok"}