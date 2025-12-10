import pytest

from core import get_key_hash


@pytest.mark.parametrize(
    'key,expected_hash',
    (
        (
            '42',
            'cf01c9d9de8cf1433d212adb97be45ecfc0fd868599faf3ee4741a5e959d424e',
        ),
        (
            'Lorem ipsum dolor sit amet',
            '52fee5030c5b61c42db2dc09435bc6e6f357aafa450c23f0c4db8f2d44c7c3a6',
        ),
        (
            'mcqL2sQBunRwaVygJBPBu8y3JcfUWA07',
            '6b13637a45c0ff387d277860dcf91bfc1b5049524062416d8ce256e019e088ea',
        ),
    ),
)
def test_get_key_hash(key, expected_hash):
    assert get_key_hash(key) == expected_hash
