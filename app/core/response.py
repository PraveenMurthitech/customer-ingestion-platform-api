# app/core/response.py

from app.core.errors import ERROR_CODES
from app.core.exceptions import AppException

def success_response(data=None, message="Success", status_code=200):
    return {
        "status": "success",
        "status_code": status_code,
        "data": data,
        "message": message
    }


def error_response(error_code: str = "INVALID_INPUT", message: str = None, status_code: int = 400):
    return {
        "status": "failure",
        "status_code": status_code,
        "data": None,
        "message": message or ERROR_CODES.get(error_code, "Something went wrong"),
        "error": {
            "code": error_code
        }
    }


def exception_response(exception: Exception):

    if isinstance(exception, AppException):
        return {
            "status": "failure",
            "status_code": exception.status_code,
            "data": None,
            "message": exception.message or ERROR_CODES.get(exception.error_code),
            "error": {
                "code": exception.error_code
            }
        }

    return {
        "status": "failure",
        "status_code": 500,
        "data": None,
        "message": ERROR_CODES.get("INTERNAL_ERROR", "Internal server error"),
        "error": {
            "code": "INTERNAL_ERROR"
        }
    }