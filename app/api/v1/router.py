from fastapi import APIRouter
from app.api.v1.endpoints import customers
from app.api.v1.endpoints import sources
from app.api.v1.endpoints import policy

api_router = APIRouter()

api_router.include_router(customers.router, tags=["Customers"])
api_router.include_router(sources.router, tags=["Sources"])
api_router.include_router(policy.router, tags=["Policy"])