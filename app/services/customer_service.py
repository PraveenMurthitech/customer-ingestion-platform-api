from app.services.common_service import insert, update
from app.dqa.customer import get_customer, list_customers
from app.core.response import success_response, exception_response
from app.core.exceptions import AppException


def create_customer_service(payload: dict):
    try:
        result = insert(payload)

        return success_response(
            data={"customer_id": result["data"]["id"]},
            message="Customer created successfully",
            status_code=201
        )

    except Exception as e:
        return exception_response(e)


def update_customer_service(customer_id: int, payload: dict):
    try:
        update(payload)

        return success_response(
            data={"customer_id": customer_id},
            message="Customer updated successfully"
        )

    except Exception as e:
        return exception_response(e)

def get_customer_service(customer_id: int):
    try:
        data = get_customer(customer_id)

        if data is None:
            raise AppException(
                error_code="CUSTOMER_NOT_FOUND",
                status_code=404
            )

        return success_response(
            data=data,
            message="Customer fetched successfully"
        )

    except AppException as e:
        return exception_response(e)

    except Exception as e:
        return exception_response(e)


def list_customers_service(limit: int, offset: int):
    try:
        data = list_customers(limit, offset)

        return success_response(
            data=data,
            message="Customers fetched successfully"
        )

    except Exception as e:
        return exception_response(e)