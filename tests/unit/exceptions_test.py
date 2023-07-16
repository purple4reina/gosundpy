import pytest

from gosundpy.exceptions import (assert_response_success, GosundException,
        GosundDeviceOfflineException)

_test_assert_response_success = (
    ({'success': True}, None),
    ({'success': False}, GosundException),
    ({'success': False, 'msg': 'device is offline'},
     GosundDeviceOfflineException),
    ({'success': False, 'msg': 'something happened'}, GosundException),
)

@pytest.mark.parametrize('response,expect', _test_assert_response_success)
def test_assert_response_success(response, expect):
    try:
        assert_response_success('testing', response)
    except Exception as e:
        assert e.__class__ == expect
    else:
        assert expect is None
