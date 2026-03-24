from fastapi import FastAPI
from app.api import api_router
from app.db.postgres import PostgresPool

app = FastAPI(
    title="Data Sync API",
    description="Customer APIs",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    PostgresPool.initialize()


@app.on_event("shutdown")
def shutdown():
    PostgresPool.close_all()

app.include_router(api_router, prefix="/api/v1")