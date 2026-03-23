# app/dqa/customer.py

from app.dqa.pg import insert_query, update_query


# 🔹 Dummy DB (in-memory simulation)
CUSTOMERS_DB = [
    {
        "id": 101,
        "customer_name": "ABC Pvt Ltd",
        "customer_email": "abc@gmail.com",
        "customer_phone": "9876543210",
        "customer_address": "Bangalore",
        "customer_state": "Karnataka",
        "customer_country": "India"
    },
    {
        "id": 102,
        "customer_name": "XYZ Pvt Ltd",
        "customer_email": "xyz@gmail.com",
        "customer_phone": "9999999999",
        "customer_address": "Mumbai",
        "customer_state": "Maharashtra",
        "customer_country": "India"
    }
]


def create_customer(data: dict):
    return insert_query("customers", data)


def update_customer(customer_id: int, data: dict):
    condition = {"id": customer_id}
    return update_query("customers", data, condition)


def get_customer(customer_id: int):
    # 🔥 simulate DB lookup
    for customer in CUSTOMERS_DB:
        if customer["id"] == customer_id:
            return customer

    return None


def list_customers(limit: int = None, offset: int = None):
    data = CUSTOMERS_DB

    # 🔹 apply pagination if given
    if offset is not None:
        data = data[offset:]

    if limit is not None:
        data = data[:limit]

    return data