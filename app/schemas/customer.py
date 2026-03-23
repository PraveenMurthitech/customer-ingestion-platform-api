from pydantic import BaseModel, EmailStr
from typing import Optional, List


# -------- REQUEST MODELS --------

class CreateCustomerRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    customer_address: str
    customer_state: Optional[str] = None
    customer_country: Optional[str] = None


class UpdateCustomerRequest(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country: Optional[str] = None


# -------- RESPONSE DATA MODELS --------

class CustomerData(BaseModel):
    id: int
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str]
    customer_address: str
    customer_state: Optional[str]
    customer_country: Optional[str]


class CustomerListItem(BaseModel):
    id: int
    customer_name: str