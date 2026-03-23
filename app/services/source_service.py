from app.services.common_service import insert, update
from app.connectors.factory import get_connector
from app.core.response import success_response, exception_response
from app.core.exceptions import AppException

from app.dqa.source import (
    get_all_sources,
    get_single_source,
    activate_source,
    deactivate_source
)


def add_source_service(customer_id: int, payload: dict):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        result = insert(payload)

        return success_response(
            data={"config_id": result["data"]["id"]},
            message="Source config added",
            status_code=201
        )

    except Exception as e:
        return exception_response(e)


def update_source_service(customer_id: int, source_name: str, payload: dict):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        update(payload)

        return success_response(
            data={
                "config_id": "uuid",
                "source_name": source_name
            },
            message="Source configuration updated successfully"
        )

    except Exception as e:
        return exception_response(e)


def test_connection_service(source_name: str, config: dict):
    try:
        if not source_name:
            raise AppException("INVALID_SOURCE", 400)

        connector = get_connector(source_name)

        if not connector:
            raise AppException("SOURCE_NOT_FOUND", 404)

        result = connector.test_connection(config)

        return success_response(
            data=result,
            message="Connection test successful"
        )

    except Exception as e:
        return exception_response(e)


def get_all_sources_service(customer_id: int):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        data = get_all_sources(customer_id)

        if not data:
            raise AppException("NO_SOURCES_FOUND", 404)

        return success_response(
            data=data,
            message="Source configurations fetched successfully"
        )

    except Exception as e:
        return exception_response(e)


def get_single_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        data = get_single_source(customer_id, source_name)

        if not data:
            raise AppException("SOURCE_NOT_FOUND", 404)

        return success_response(
            data=data,
            message="Source configuration fetched successfully"
        )

    except Exception as e:
        return exception_response(e)


def activate_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        result = activate_source(customer_id, source_name)

        if not result:
            raise AppException("SOURCE_NOT_FOUND", 404)

        return success_response(
            data={},
            message="Source activated successfully"
        )

    except Exception as e:
        return exception_response(e)


def deactivate_source_service(customer_id: int, source_name: str):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_name:
            raise AppException("SOURCE_NOT_FOUND", 404)

        result = deactivate_source(customer_id, source_name)

        if not result:
            raise AppException("SOURCE_NOT_FOUND", 404)

        return success_response(
            data={},
            message="Source deactivated successfully"
        )

    except Exception as e:
        return exception_response(e)