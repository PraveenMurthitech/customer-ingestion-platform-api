# app/dqa/pg.py

def insert_query(table: str, data: dict):

    return {
        "status": "success",
        "status_code": 201,
        "data": {"id": 101},
        "message": f"Inserted into {table}"
    }


def update_query(table: str, data: dict, condition: dict):

    return {
        "status": "success",
        "status_code": 200,
        "data": {},
        "message": f"Updated {table}"
    }