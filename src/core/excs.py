from fastapi import HTTPException, status


class LimitExceeded(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, 'Limit exceeded')


class NotFound(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, f'{name} not found')
