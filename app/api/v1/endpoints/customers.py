from fastapi import APIRouter, Path, Query
from app.schemas.customer import (
    CreateCustomerRequest,
    UpdateCustomerRequest
)
from app.services.customer_service import (
    create_customer_service,
    update_customer_service,
    get_customer_service,
    list_customers_service
)

router = APIRouter()


@router.post(
    "/customers",
    summary="Create Customer",
    description="Creates a new customer (tenant) in the system."
)
def create_customer(payload: CreateCustomerRequest):
    return create_customer_service(payload.dict())


@router.put(
    "/customers/{customer_id}",
    summary="Update Customer",
    description="Updates customer details like name, phone, or address."
)
def update_customer(
    customer_id: int = Path(..., description="Customer ID"),
    payload: UpdateCustomerRequest = None
):
    return update_customer_service(customer_id, payload.dict(exclude_unset=True))


@router.get(
    "/customers/{customer_id}",
    summary="Get Customer Details",
    description="Fetch complete details of a specific customer."
)
def get_customer(customer_id: int = Path(...)):
    return get_customer_service(customer_id)


@router.get(
    "/customers",
    summary="List Customers",
    description="Returns list of all customers"
)
def list_customers(
    limit: int = Query(10),
    offset: int = Query(0)
):
    return list_customers_service(limit, offset)