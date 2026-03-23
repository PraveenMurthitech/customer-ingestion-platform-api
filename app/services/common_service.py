def insert(data: dict):
    return {
        "status": "success",
        "status_code": 201,
        "data": {"customer_id": 101},
        "message": "Customer created successfully"
    }


def update(data: dict):
    return {
        "status": "success",
        "status_code": 200,
        "data": {"customer_id": 101},
        "message": "Customer updated successfully"
    }