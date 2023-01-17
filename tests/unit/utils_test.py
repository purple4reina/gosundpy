import pytest
import time

from gosundpy.utils import cache_response

_test_cache_value = (
        {'seconds': 3600},
        {'minutes': 60},
        {'seconds': 1800, 'minutes': 30},
        {'hours': 1},
        {'hours': 0.5, 'minutes': 30},
)

@pytest.mark.parametrize('kwargs', _test_cache_value)
def test_cache_response(kwargs, monkeypatch):
    call_count = [0]

    @cache_response(**kwargs)
    def test_fn():
        call_count[0] += 1
        return call_count[0]

    for _ in range(3):
        actual = test_fn()
        assert actual == 1, 'wrong value returned'

    now = time.time()
    monkeypatch.setattr('time.time', lambda: now + 3601)

    for _ in range(3):
        actual = test_fn()
        assert actual == 2, 'wrong value returned'

    test_fn.clear_cache()

    for _ in range(3):
        actual = test_fn()
        assert actual == 3, 'wrong value returned'
