from pydantic import BaseModel
from typing import Dict, Any, List, Optional


# -------- REQUEST MODELS --------

class AddSourceRequest(BaseModel):
    source_name: str
    config: Dict[str, Any]


class UpdateSourceRequest(BaseModel):
    config: Dict[str, Any]


class TestConnectionRequest(BaseModel):
    source_name: str
    config: Dict[str, Any]


# -------- RESPONSE MODELS --------

class SourceConfigItem(BaseModel):
    config_id: str
    source_name: str
    version: int
    is_active: bool


class SourceConfigDetail(BaseModel):
    config_id: str
    customer_id: int
    source_name: str
    version: int
    config: Dict[str, Any]
    checksum: str
    is_active: bool
    created_at: str
    updated_at: str