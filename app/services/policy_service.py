from app.db.dqa.policy import PolicyDAO
from app.core.response import success_response, exception_response
from app.core.exceptions import AppException

dao = PolicyDAO()


# 🔹 CREATE POLICIES (BULK)
def create_policies_service(customer_id: int, payload: dict):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not payload:
            raise AppException("INVALID_PAYLOAD", 400)

        source_id = payload.get("source_id")
        policies = payload.get("policies")

        if not source_id:
            raise AppException("SOURCE_NOT_FOUND", 404)

        if not policies or not isinstance(policies, list):
            raise AppException("POLICIES_REQUIRED", 400)

        # 🔴 Validate each policy
        for policy in policies:
            if not policy.get("module_name"):
                raise AppException("MODULE_NAME_REQUIRED", 400)

            if policy.get("ingestion_type") not in ["bulk", "incremental"]:
                raise AppException("INVALID_INGESTION_TYPE", 400)

            if not isinstance(policy.get("interval_seconds"), int):
                raise AppException("INVALID_INTERVAL", 400)

        # ⚠️ temp fallback (bad schema design)
        customer_name = payload.get("customer_name", "unknown")

        result = dao.insert_bulk(customer_id, customer_name, source_id, policies)

        if not result:
            raise AppException(
                error_code="POLICY_CREATION_FAILED",
                message="No policies were created",
                status_code=500
            )

        return success_response(
            data={
                "customer_id": customer_id,
                "source_id": source_id,
                "created_policies": result,
                "created_count": len(result)
            },
            message="Ingestion policies created successfully",
            status_code=201
        )

    except Exception as e:
        return exception_response(e)


# 🔹 UPDATE POLICY
def update_policy_service(policy_id: str, payload: dict):
    try:
        if not policy_id:
            raise AppException("POLICY_ID_REQUIRED", 400)

        if not payload:
            raise AppException("INVALID_PAYLOAD", 400)

        # 🔴 Validate optional fields
        if "ingestion_type" in payload:
            if payload["ingestion_type"] not in ["bulk", "incremental"]:
                raise AppException("INVALID_INGESTION_TYPE", 400)

        if "interval_seconds" in payload:
            if not isinstance(payload["interval_seconds"], int):
                raise AppException("INVALID_INTERVAL", 400)

        if "is_active" in payload:
            if not isinstance(payload["is_active"], bool):
                raise AppException("INVALID_IS_ACTIVE", 400)

        result = dao.update(policy_id, payload)

        if not result:
            raise AppException(
                error_code="POLICY_NOT_FOUND",
                status_code=404
            )

        return success_response(
            data=result,
            message="Ingestion policy updated successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 ACTIVATE POLICY
def activate_policy_service(policy_id: str):
    try:
        if not policy_id:
            raise AppException("POLICY_ID_REQUIRED", 400)

        result = dao.set_active(policy_id, True)

        if not result:
            raise AppException("POLICY_NOT_FOUND", 404)

        return success_response(
            data={
                "policy_id": result["id"],
                "is_active": result["is_active"]
            },
            message="Policy activated successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 DEACTIVATE POLICY
def deactivate_policy_service(policy_id: str):
    try:
        if not policy_id:
            raise AppException("POLICY_ID_REQUIRED", 400)

        result = dao.set_active(policy_id, False)

        if not result:
            raise AppException("POLICY_NOT_FOUND", 404)

        return success_response(
            data={
                "policy_id": result["id"],
                "is_active": result["is_active"]
            },
            message="Policy deactivated successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 GET SINGLE POLICY
def get_policy_service(policy_id: str):
    try:
        if not policy_id:
            raise AppException("POLICY_ID_REQUIRED", 400)

        data = dao.get(policy_id)

        if not data:
            raise AppException(
                error_code="POLICY_NOT_FOUND",
                status_code=404
            )

        return success_response(
            data=data,
            message="Policy fetched successfully"
        )

    except Exception as e:
        return exception_response(e)


# 🔹 LIST POLICIES
def list_policies_service(customer_id: int, source_id: int):
    try:
        if not customer_id:
            raise AppException("CUSTOMER_NOT_FOUND", 404)

        if not source_id:
            raise AppException("SOURCE_NOT_FOUND", 404)

        data = dao.list(customer_id, source_id)

        # 🔥 CRITICAL FIX (your original issue)
        if not data:
            raise AppException(
                error_code="NO_POLICIES_FOUND",
                message="No ingestion policies found for this customer and source",
                status_code=404
            )

        return success_response(
            data=data,
            message="Policies fetched successfully"
        )

    except Exception as e:
        return exception_response(e)