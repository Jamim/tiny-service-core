import pytest
from fastapi import HTTPException, status

from core.excs import LimitExceeded, NotFound


@pytest.mark.parametrize(
    'exception,status_code,detail',
    (
        (LimitExceeded, status.HTTP_403_FORBIDDEN, 'Limit exceeded'),
        (NotFound('Dummy'), status.HTTP_404_NOT_FOUND, 'Dummy not found'),
    ),
)
def test_excs(exception, status_code, detail):
    try:
        raise exception
    except HTTPException as exc:
        assert exc.status_code == status_code
        assert exc.detail == detail
