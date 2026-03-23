from fastapi import APIRouter
from app.api.v1.endpoints import customers, sources

api_router = APIRouter()

api_router.include_router(customers.router, tags=["Customers"])
api_router.include_router(sources.router, tags=["Sources"])