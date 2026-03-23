from fastapi import APIRouter, Path
from app.schemas.source import (
    AddSourceRequest,
    UpdateSourceRequest,
    TestConnectionRequest
)
from app.services.source_service import (
    add_source_service,
    update_source_service,
    test_connection_service,
    get_all_sources_service,
    get_single_source_service,
    activate_source_service,
    deactivate_source_service
)

router = APIRouter()


@router.post(
    "/customers/{customer_id}/sources",
    summary="Add Source Configuration",
    description="Adds configuration for a data source (e.g., Zoho, Tally)."
)
def add_source(customer_id: int, payload: AddSourceRequest):
    return add_source_service(customer_id, payload.dict())


@router.put(
    "/customers/{customer_id}/sources/{source_name}",
    summary="Update Source Configuration",
    description="Updates existing source configuration."
)
def update_source(customer_id: int, source_name: str, payload: UpdateSourceRequest):
    return update_source_service(customer_id, source_name, payload.dict())


@router.post(
    "/sources/test-connection",
    summary="Test Source Connection",
    description="Validates source connection without storing config."
)
def test_connection(payload: TestConnectionRequest):
    return test_connection_service(payload.source_name, payload.config)


@router.get(
    "/customers/{customer_id}/sources",
    summary="Get All Source Configurations"
)
def get_all_sources(customer_id: int):
    return get_all_sources_service(customer_id)


@router.get(
    "/customers/{customer_id}/sources/{source_name}",
    summary="Get Single Source Configuration"
)
def get_single_source(customer_id: int, source_name: str):
    return get_single_source_service(customer_id, source_name)


@router.patch(
    "/customers/{customer_id}/sources/{source_name}/activate",
    summary="Activate Source Configuration"
)
def activate_source(customer_id: int, source_name: str):
    return activate_source_service(customer_id, source_name)


@router.patch(
    "/customers/{customer_id}/sources/{source_name}/deactivate",
    summary="Deactivate Source Configuration"
)
def deactivate_source(customer_id: int, source_name: str):
    return deactivate_source_service(customer_id, source_name)