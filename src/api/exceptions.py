from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """Exception raised for bad requests."""

    def __init__(self, message: str, detail: str = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.message = message
