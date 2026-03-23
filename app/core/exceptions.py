# app/core/exceptions.py

class AppException(Exception):
    def __init__(
        self,
        error_code: str,
        status_code: int = 400,
        message: str = None
    ):
        """
        Custom application exception

        :param error_code: predefined error code (from errors.py)
        :param status_code: HTTP status code (default: 400)
        :param message: optional custom message
        """
        self.error_code = error_code
        self.status_code = status_code
        self.message = message

        super().__init__(self.message or error_code)