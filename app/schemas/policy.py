from pydantic import BaseModel, Field
from typing import List, Optional


# 🔹 POLICY ITEM (used inside bulk create)
class PolicyItem(BaseModel):
    module_name: str = Field(..., example="Leads")
    ingestion_type: str = Field(..., example="incremental")
    interval_seconds: int = Field(..., gt=0, example=300)
    table_name: Optional[str] = Field(None, example="zoho_leads")


# 🔹 CREATE POLICIES REQUEST
class CreatePoliciesRequest(BaseModel):
    source_id: int = Field(..., example=1)
    customer_name: Optional[str] = Field(None, example="Praveen")
    policies: List[PolicyItem]


# 🔹 UPDATE POLICY REQUEST
class UpdatePolicyRequest(BaseModel):
    ingestion_type: Optional[str] = None
    interval_seconds: Optional[int] = None
    is_active: Optional[bool] = None
    table_name: Optional[str] = None