from app.db.postgres import get_db_cursor
from app.core.exceptions import AppException
import uuid
import json


class SourceDAO:

    def insert(self, data: dict):
        try:
            if "config" in data:
                data["config"] = json.dumps(data["config"])

            columns = list(data.keys())
            values = list(data.values())

            query = f"""
                INSERT INTO customer_ingestion_config ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(values))})
                RETURNING customer_id, source_name;
            """

            with get_db_cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()

            return {
                "customer_id": result[0],
                "source_name": result[1],
                "action": "created"
            }

        except Exception as e:
            print("INSERT FAILED:", str(e))
            raise AppException(
                error_code="SOURCE_INSERT_FAILED",
                message="Failed to insert source config",
                status_code=500
            )

    # 🔹 GET ALL
    def get_all(self, customer_id: int):
        try:
            query = """
                SELECT * FROM customer_ingestion_config
                WHERE customer_id = %s;
            """

            with get_db_cursor(dict_cursor=True) as cursor:
                cursor.execute(query, (customer_id,))
                return cursor.fetchall()

        except Exception as e:
            print("GET ALL FAILED:", str(e))
            raise AppException("SOURCE_FETCH_FAILED", 500)

    # 🔹 GET SINGLE
    def get_single(self, customer_id: int, source_name: str):
        try:
            query = """
                SELECT * FROM customer_ingestion_config
                WHERE customer_id = %s AND source_name = %s;
            """

            with get_db_cursor(dict_cursor=True) as cursor:
                cursor.execute(query, (customer_id, source_name))
                return cursor.fetchone()

        except Exception as e:
            print("GET SINGLE FAILED:", str(e))
            raise AppException("SOURCE_FETCH_FAILED", 500)

    # 🔹 UPDATE
    def update(self, customer_id: int, source_name: str, data: dict):
        try:
            if not data:
                raise ValueError("Update data cannot be empty")

            if "config" in data:
                data["config"] = json.dumps(data["config"])

            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            values = list(data.values())

            query = f"""
                UPDATE customer_ingestion_config
                SET {set_clause}, updated_at = NOW()
                WHERE customer_id = %s AND source_name = %s;
            """

            with get_db_cursor() as cursor:
                cursor.execute(query, values + [customer_id, source_name])

                if cursor.rowcount == 0:
                    raise AppException(
                        error_code="SOURCE_NOT_FOUND",
                        status_code=404
                    )

            return True

        except AppException:
            raise

        except Exception as e:
            raise AppException("SOURCE_UPDATE_FAILED", 500)

    # 🔹 ACTIVATE
    def activate(self, customer_id: int, source_name: str):
        return self._set_active(customer_id, source_name, True)

    # 🔹 DEACTIVATE
    def deactivate(self, customer_id: int, source_name: str):
        return self._set_active(customer_id, source_name, False)

    # 🔹 INTERNAL
    def _set_active(self, customer_id: int, source_name: str, is_active: bool):
        try:
            query = """
                UPDATE customer_ingestion_config
                SET is_active = %s, updated_at = NOW()
                WHERE customer_id = %s AND source_name = %s;
            """

            with get_db_cursor() as cursor:
                cursor.execute(query, (is_active, customer_id, source_name))

                if cursor.rowcount == 0:
                    raise AppException(
                        error_code="SOURCE_NOT_FOUND",
                        status_code=404
                    )

            return True

        except AppException:
            raise

        except Exception as e:
            print("ACTIVATE/DEACTIVATE FAILED:", str(e))
            raise AppException("SOURCE_STATUS_UPDATE_FAILED", 500)