# app/dqa/pg.py

def insert_query(table: str, data: dict):
    print(f"[DB INSERT] Table: {table} | Data: {data}")

    return {
        "status": "success",
        "status_code": 201,
        "data": {"id": 101},
        "message": f"Inserted into {table}"
    }


def update_query(table: str, data: dict, condition: dict):
    print(f"[DB UPDATE] Table: {table} | Data: {data} | Condition: {condition}")

    return {
        "status": "success",
        "status_code": 200,
        "data": {},
        "message": f"Updated {table}"
    }