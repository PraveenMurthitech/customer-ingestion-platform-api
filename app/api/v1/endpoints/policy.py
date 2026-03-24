from fastapi import APIRouter, Path, Query, Body
from app.services.policy_service import (
    create_policies_service,
    update_policy_service,
    activate_policy_service,
    deactivate_policy_service,
    get_policy_service,
    list_policies_service
)

from app.schemas.policy import (
    CreatePoliciesRequest,
    UpdatePolicyRequest
)

router = APIRouter()


# 🔹 12. CREATE POLICIES (BULK)
@router.post("/customers/{customer_id}/policies")
def create_policies(
    customer_id: int = Path(...),
    payload: CreatePoliciesRequest = Body(...)
):
    return create_policies_service(customer_id, payload.dict())


# 🔹 13. UPDATE POLICY
@router.put("/policies/{policy_id}")
def update_policy(
    policy_id: str = Path(...),
    payload: UpdatePolicyRequest = Body(...)
):
    return update_policy_service(policy_id, payload.dict(exclude_unset=True))


# 🔹 14. ACTIVATE POLICY
@router.patch("/policies/{policy_id}/activate")
def activate_policy(
    policy_id: str = Path(...)
):
    return activate_policy_service(policy_id)


# 🔹 15. DEACTIVATE POLICY
@router.patch("/policies/{policy_id}/deactivate")
def deactivate_policy(
    policy_id: str = Path(...)
):
    return deactivate_policy_service(policy_id)


# 🔹 GET SINGLE POLICY
@router.get("/policies/{policy_id}")
def get_policy(
    policy_id: str = Path(...)
):
    return get_policy_service(policy_id)


# 🔹 LIST POLICIES
@router.get("/customers/{customer_id}/policies")
def list_policies(
    customer_id: int = Path(...),
    source_id: int = Query(...)
):
    return list_policies_service(customer_id, source_id)