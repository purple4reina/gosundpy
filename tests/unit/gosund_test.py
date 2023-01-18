import pytest
import responses

from conftest import patch_status, patch_get_device, BASEURL
from gosundpy.exceptions import GosundException

@responses.activate
def test_gosund_get_device_status_success(gosund, gosund_device):
    status = [{'code': 'abc', 'value': 123}, {'code': '123', 'value': 'abc'}]
    resp_json = {'success': True, 'result': [{'id': gosund_device.device_id, 'status': status}]}
    patch_status(gosund_device.device_id, resp_json=resp_json)
    assert gosund.get_device_status(gosund_device.device_id) == status

@responses.activate
def test_gosund_get_device_status_failure(gosund, gosund_device):
    msg = 'oops'
    resp_json = {'success': False, 'msg': msg}
    patch_status(gosund_device.device_id, resp_json=resp_json)
    try:
        gosund.get_device_status(gosund_device.device_id)
    except GosundException as e:
        assert e.args == (f'unable to get device statuses: {msg}',)
    else:
        raise AssertionError('should have raised a GosundException')

@responses.activate
def test_gosund_get_device_status_not_found(gosund, gosund_device):
    resp_json = {'success': True, 'result': [{'id': 'wrong', 'status': []}]}
    patch_status(gosund_device.device_id, resp_json=resp_json)
    try:
        gosund.get_device_status(gosund_device.device_id)
    except GosundException as e:
        assert e.args == ('unable to find status for device with id '
                f'"{gosund_device.device_id}"',)
    else:
        raise AssertionError('should have raised a GosundException')

@responses.activate
def test_gosund_get_device_statuses_success(gosund, gosund_device):
    status = [{'code': 'abc', 'value': 123}, {'code': '123', 'value': 'abc'}]
    resp_json = {'success': True, 'result': [{'id': gosund_device.device_id, 'status': status}]}
    patch_status(gosund_device.device_id, resp_json=resp_json)
    assert gosund.get_device_statuses() == {gosund_device.device_id: status}

@responses.activate
def test_gosund_get_device_statuses_failure(gosund, gosund_device):
    msg = 'oops'
    resp_json = {'success': False, 'msg': msg}
    patch_status(gosund_device.device_id, resp_json=resp_json)
    try:
        gosund.get_device_statuses()
    except GosundException as e:
        assert e.args == (f'unable to get device statuses: {msg}',)
    else:
        raise AssertionError('should have raised a GosundException')

_test_device_id_1 = 'device-id-1'
_test_device_id_2 = 'device-id-2'
_test_device_id_3 = 'device-id-3'
_test_status_1 = [{'code': 'abc', 'value': _test_device_id_1}]
_test_status_2 = [{'code': 'abc', 'value': _test_device_id_2}]
_test_status_3 = [{'code': 'abc', 'value': _test_device_id_3}]

def _patch_testing_requests():
    _test_result_1 = {'id': _test_device_id_1, 'status': _test_status_1}
    _test_result_2 = {'id': _test_device_id_2, 'status': _test_status_2}
    _test_result_3 = {'id': _test_device_id_3, 'status': _test_status_3}

    patch_get_device(_test_device_id_1, 'ab')
    patch_get_device(_test_device_id_2, 'ab')
    patch_get_device(_test_device_id_3, 'ab')

    def _patch_status_for(device_ids, results):
        patch_status(*device_ids, resp_json={'success': True, 'result': results})

    _patch_status_for([], [])
    _patch_status_for([_test_device_id_1], [_test_result_1])
    _patch_status_for([_test_device_id_1, _test_device_id_2],
            [_test_result_1, _test_result_2])
    _patch_status_for([_test_device_id_1, _test_device_id_2, _test_device_id_3],
            [_test_result_1, _test_result_2, _test_result_3])

    responses.add(
            responses.POST,
            f'{BASEURL}/devices/{_test_device_id_1}/commands',
            json={'success': True},
            status=200,
    )

@responses.activate
def test_gosund_get_device_statuses_device_ids(gosund):
    _patch_testing_requests()

    # no devices
    assert gosund.get_device_statuses() == {}

    # one device added
    gosund.get_device(_test_device_id_1)
    assert gosund.get_device_statuses() == {
            _test_device_id_1: _test_status_1,
    }

    # second device added
    gosund.get_device(_test_device_id_2)
    assert gosund.get_device_statuses() == {
            _test_device_id_1: _test_status_1,
            _test_device_id_2: _test_status_2,
    }

    # third device added
    gosund.get_device(_test_device_id_3)
    assert gosund.get_device_statuses() == {
            _test_device_id_1: _test_status_1,
            _test_device_id_2: _test_status_2,
            _test_device_id_3: _test_status_3,
    }

@responses.activate
def test_gosund_get_device_statuses_cache(gosund):
    _patch_testing_requests()

    gosund.get_device(_test_device_id_1)
    resp1 = gosund.get_device_statuses()
    resp2 = gosund.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}
    assert id(resp1) == id(resp2)

@responses.activate
def test_gosund_get_device_statuses_cache_remove(gosund):
    _patch_testing_requests()

    gosund.get_device(_test_device_id_1)
    resp1 = gosund.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}

    gosund._remove_known_device(_test_device_id_1)
    resp2 = gosund.get_device_statuses()
    assert resp2 == {}

@responses.activate
def test_gosund_get_device_statuses_cache_clear(gosund):
    _patch_testing_requests()

    gosund.get_device(_test_device_id_1)
    resp1 = gosund.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}

    gosund._clear_statuses_cache()
    resp2 = gosund.get_device_statuses()
    assert resp2 == {_test_device_id_1: _test_status_1}
    assert id(resp1) != id(resp2)

@responses.activate
def test_gosund_get_device_statuses_cache_send_commands(gosund):
    _patch_testing_requests()

    gosund.get_device(_test_device_id_1)
    resp1 = gosund.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}

    gosund.send_commands(_test_device_id_1, [])
    resp2 = gosund.get_device_statuses()
    assert resp2 == {_test_device_id_1: _test_status_1}
    assert id(resp1) != id(resp2)

@responses.activate
def test_gosund_get_device_statuses_cache_per_instance(gosund, gosund2):
    _patch_testing_requests()

    gosund.get_device(_test_device_id_1)
    resp1 = gosund.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}

    resp2 = gosund2.get_device_statuses()
    assert resp2 == {}
    assert id(resp1) != id(resp2)

@responses.activate
def test_gosund_get_device_statuses_non_caching(gosund_non_caching):
    _patch_testing_requests()

    gosund_non_caching.get_device(_test_device_id_1)
    resp1 = gosund_non_caching.get_device_statuses()
    resp2 = gosund_non_caching.get_device_statuses()
    assert resp1 == {_test_device_id_1: _test_status_1}
    assert id(resp1) != id(resp2)
