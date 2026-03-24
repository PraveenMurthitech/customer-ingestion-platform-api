from app.db.dqa.source import SourceDAO
from app.connectors.factory import get_connector
from app.core.response import success_response, exception_response
from app.core.exceptions import AppException


dao = SourceDAO()


# 🔹 ADD SOURCE
def add_source_service(customer_id: int, payload: dict):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not payload:
            raise AppException("INVALID_PAYLOAD", 400)

        payload["customer_id"] = customer_id

        result = dao.insert(payload)

        return success_response(
            data=result,  # ✅ FIXED (no {})
            message="Source config added",
            status_code=201
        )

    except AppException as e:
        return exception_response(e)

    except Exception as e:
        return exception_response(
            AppException(
                error_code="INTERNAL_SERVER_ERROR",
                status_code=500
            )
        )


# 🔹 UPDATE SOURCE
def update_source_service(customer_id: int, source_name: str, payload: dict):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        dao.update(customer_id, source_name, payload)

        return success_response(
            data={
                "customer_id": customer_id,
                "source_name": source_name
            },
            message="Source configuration updated successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 TEST CONNECTION (this part was fine)
def test_connection_service(source_name: str, config: dict):
    try:
        if not source_name:
            raise AppException("INVALID_SOURCE", 400)

        connector = get_connector(source_name)

        result = connector.test_connection(config)

        return success_response(
            data=result,
            message="Connection test successful"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 GET ALL SOURCES
def get_all_sources_service(customer_id: int):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        data = dao.get_all(customer_id)

        if not data:
            raise AppException("NO_SOURCES_FOUND", 404)

        return success_response(
            data=data,
            message="Source configurations fetched successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 GET SINGLE SOURCE
def get_single_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        data = dao.get_single(customer_id, source_name)

        if not data:
            raise AppException("SOURCE_NOT_FOUND", 404)

        return success_response(
            data=data,
            message="Source configuration fetched successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 ACTIVATE
def activate_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        dao.activate(customer_id, source_name)

        return success_response(
            data={},
            message="Source activated successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 DEACTIVATE
def deactivate_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        dao.deactivate(customer_id, source_name)

        return success_response(
            data={},
            message="Source deactivated successfully"
        )

    except Exception as e:
        return exception_response(e)