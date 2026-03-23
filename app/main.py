from fastapi import FastAPI
from app.api import api_router

app = FastAPI(
    title="Data Sync API",
    description="Customer APIs",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")