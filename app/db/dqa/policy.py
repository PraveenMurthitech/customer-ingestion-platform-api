from ..postgres import get_db_cursor
from app.core.exceptions import AppException
from datetime import datetime, timedelta


class PolicyDAO:

    # 🔹 BULK INSERT
    def insert_bulk(self, customer_id: int, customer_name: str, source_id: int, policies: list):
        if not policies:
            raise ValueError("Policies list cannot be empty")

        created_policies = []

        try:
            with get_db_cursor(dict_cursor=True) as cursor:

                for policy in policies:
                    next_run_at = datetime.utcnow() + timedelta(
                        seconds=policy["interval_seconds"]
                    )

                    query = """
                        INSERT INTO customer_ingestion_policy (
                            customer_id,
                            customer_name,
                            source_id,
                            module_name,
                            ingestion_type,
                            interval_seconds,
                            next_run_at,
                            table_name
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id, module_name, ingestion_type, interval_seconds, is_active;
                    """

                    values = (
                        customer_id,
                        customer_name,
                        source_id,
                        policy["module_name"],
                        policy["ingestion_type"],
                        policy["interval_seconds"],
                        next_run_at,
                        policy.get("table_name")
                    )

                    cursor.execute(query, values)
                    result = cursor.fetchone()

                    created_policies.append({
                        "policy_id": result["id"],
                        "module_name": result["module_name"],
                        "ingestion_type": result["ingestion_type"],
                        "interval_seconds": result["interval_seconds"],
                        "is_active": result["is_active"]
                    })

            return created_policies

        except Exception as e:
            print("POLICY INSERT FAILED:", str(e))
            raise AppException(
                error_code="POLICY_INSERT_FAILED",
                message="Failed to insert ingestion policies",
                status_code=500
            )

    # 🔹 UPDATE POLICY
    def update(self, policy_id: str, data: dict):
        if not data:
            raise ValueError("Update data cannot be empty")

        try:
            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            values = list(data.values())

            query = f"""
                UPDATE customer_ingestion_policy
                SET {set_clause}, updated_at = NOW()
                WHERE id = %s
                RETURNING id, ingestion_type, interval_seconds, is_active, updated_at;
            """

            with get_db_cursor(dict_cursor=True) as cursor:
                cursor.execute(query, values + [policy_id])
                result = cursor.fetchone()

                if not result:
                    raise AppException(
                        error_code="POLICY_NOT_FOUND",
                        status_code=404
                    )

            return result

        except AppException:
            raise

        except Exception as e:
            print("POLICY UPDATE FAILED:", str(e))
            raise AppException(
                error_code="POLICY_UPDATE_FAILED",
                message="Failed to update policy",
                status_code=500
            )

    # 🔹 ACTIVATE / DEACTIVATE
    def set_active(self, policy_id: str, is_active: bool):
        try:
            query = """
                UPDATE customer_ingestion_policy
                SET is_active = %s,
                    inactive_at = CASE WHEN %s = false THEN NOW() ELSE NULL END,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id, is_active;
            """


            with get_db_cursor(dict_cursor=True) as cursor:
                cursor.execute(query, (is_active, is_active, policy_id))
                result = cursor.fetchone()

                if not result:
                    raise AppException(
                        error_code="POLICY_NOT_FOUND",
                        status_code=404
                    )

            return result

        except Exception as e:
            print("POLICY STATUS FAILED:", str(e))
            raise AppException(
                error_code="POLICY_STATUS_UPDATE_FAILED",
                message="Failed to update policy status",
                status_code=500
            )

    # 🔹 GET SINGLE POLICY
    def get(self, policy_id: str):
        query = """
            SELECT * FROM customer_ingestion_policy
            WHERE id = %s;
        """

        with get_db_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (policy_id,))
            return cursor.fetchone()

    # 🔹 LIST POLICIES (optional but useful)
    def list(self, customer_id: int, source_id: int):
        query = """
            SELECT * FROM customer_ingestion_policy
            WHERE customer_id = %s AND source_id = %s
            ORDER BY created_at DESC;
        """

        with get_db_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (customer_id, source_id))
            return cursor.fetchall()