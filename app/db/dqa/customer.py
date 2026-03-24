from ..postgres import get_db_cursor
from app.core.exceptions import AppException


class CustomerDAO:

    def insert(self, data: dict):
        if not data:
            raise ValueError("Insert data cannot be empty")

        columns = list(data.keys())
        values = list(data.values())

        query = f"""
            INSERT INTO customer_master ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(values))})
            RETURNING id;
        """

        try:

            with get_db_cursor() as cursor:
                cursor.execute(query, values)
                inserted_id = cursor.fetchone()[0]

            return {"id": inserted_id}

        except Exception as e:
            # 🔥 Log properly (replace print with logger later)
            print("DB INSERT FAILED:", str(e))

            # ⚠️ Don't leak raw DB errors to API layer
            raise AppException(
                error_code="DB_INSERT_FAILED",
                message="Failed to insert customer",
                status_code=500
            )

    def update(self, customer_id: int, data: dict):
        if not data:
            raise ValueError("Update data cannot be empty")

        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())

        query = f"""
            UPDATE customer_master
            SET {set_clause}
            WHERE id = %s;
        """

        with get_db_cursor() as cursor:
            cursor.execute(query, values + [customer_id])

            if cursor.rowcount == 0:
                raise Exception("Customer not found")

        return {"id": customer_id}

    def delete(self, customer_id: int):
        query = """
            DELETE FROM customer_master
            WHERE id = %s;
        """

        with get_db_cursor() as cursor:
            cursor.execute(query, (customer_id,))

            if cursor.rowcount == 0:
                raise Exception("Customer not found")

        return {"id": customer_id}

    def get(self, customer_id: int):
        query = """
            SELECT * FROM customer_master
            WHERE id = %s;
        """

        with get_db_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (customer_id,))
            return cursor.fetchone()

    def list(self, limit: int, offset: int):
        query = """
            SELECT * FROM customer_master
            ORDER BY id
            LIMIT %s OFFSET %s;
        """

        with get_db_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, (limit, offset))
            return cursor.fetchall()